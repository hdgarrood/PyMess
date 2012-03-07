'''
Chat server based on the BasicTCPServer class in this package. Overrides a 
few of its methods in order to send messages welcoming new clients,
notifying of clients leaving, and also to store a dictionary of client names.
'''

import queue
import socket
import server.basictcpserver as bts

class ChatServer(bts.BasicTCPServer):
    
    def __init__(self, server_address=(socket.gethostname(),8882), bind_and_activate=True):
        super().__init__(server_address, bind_and_activate)
        self.client_names = {}
        self.client_names[self.srvsock] = "Server"
        self.client_commands = {"say":self.broadcast_message, "name":self.rename_client}
        self.welcome_message = "Welcome to the python chatserver.\n"
            
    def process_data(self):
        for rsock in self.read_queues:
            try:
                message = self.read_queues[rsock].get_nowait()
            except queue.Empty:
                continue
            
            splitMessage = message.rstrip('\r\n').partition(' ')
            
            try:
                self.client_commands[splitMessage[0]](rsock, splitMessage[2])
            except KeyError:
                self.send_message(rsock, "Invalid command. Commands are:\nsay\nname\n")
         
    def send_message(self, recipient, message):
        if recipient in self.write_queues:
            self.write_queues[recipient].put(message)            
    
    def broadcast_message(self, client, message):
        if message:
            formattedMessage = "[{}] {}\n".format(self.client_names[client], message)
            for wsock in self.write_queues:
                self.write_queues[wsock].put(formattedMessage)
            
    def accept_new_connection(self, srvsock):
        new_sock = super().accept_new_connection(srvsock)
        self.client_names[new_sock] = "Anonymous"
        self.broadcast_message(self.srvsock, "New connection from {}".format(new_sock.getpeername()[0]))
        
    def terminate_connection(self, sock, reason=None):
        super().terminate_connection(sock, reason)
        self.broadcast_message(self.srvsock, "{} left".format(self.client_names[sock]))
    
    def rename_client(self, client, message):
        if message not in ("", "Server"):
            self.broadcast_message(self.srvsock,
                                   "{} renamed to {}".format(self.client_names[client], message))
            self.client_names[client] = message
