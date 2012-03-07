'''
A basic TCP server. Has a list of clients (self.clients) which is
managed automatically whenever a client connects or disconnects.
Also contains read and write queues for each client; a subclass
of this class should simply implement the process_data method
for the bulk of its functionality, reading from self.read_queues
and writing to self.write_queues instead of trying to send data
manually.
'''

import socket
import queue
import select
import logging

logger = logging.getLogger('serverLogger')

class BasicTCPServer:
    def __init__(self, server_address=(socket.gethostname(),8882), bind_and_activate=True):
        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvsock.setblocking(0)
        self.server_address = server_address
        self.select_timeout = 1

        self.clients = []
        self.read_queues = {}
        self.write_queues = {}
        
        self.welcome_message = "Welcome to the python server."

        if bind_and_activate:
            self.bind_and_activate()

    def bind_and_activate(self):
        try:
            self.srvsock.bind(self.server_address)
            self.srvsock.listen(5)
        except socket.error as err:
            logger.warning("Could not bind socket:")
            logger.warning(err)
            if err.errno == 10048: # Socket already in use
                host, port = self.server_address
                self.server_address = host, port + 1
                logger.info("Retrying on port %s", self.server_address[1])
                self.bind_and_activate()
        else:
            logger.info("%s listening on %s", self.__class__.__name__, self.server_address)
            
    def inputs(self):
        inputs = list(self.clients)
        inputs.append(self.srvsock)
        return inputs
    
    def outputs(self):
        return self.clients

    def serve_forever(self):
        logger.info("Serving forever...")
        while self.srvsock:
            try:
                inputs, outputs = self.inputs(), self.outputs()
                reads, writes, exceptions = select.select(inputs,
                                                          outputs,
                                                          inputs,
                                                          self.select_timeout)
                
                broken_connections = self.handle_reads(reads)
                self.process_data()
                
                # Don't try to write to any socks which have been removed
                for sock in broken_connections:
                    if sock in writes:
                        writes.remove(sock)
                        
                self.send_writes(writes)
                self.handle_exceptions(exceptions)
                
            except KeyboardInterrupt:
                logger.info("Received keyboard interrupt. Shutting server down...")
                self.shutdown()
                return

    def handle_reads(self, reads):
        broken_connections = []
        for sock in reads:
            if sock is self.srvsock:
                self.accept_new_connection(sock)
            else:
                try:
                    data = sock.recv(4096)
                    message = data.decode()
                except UnicodeDecodeError as err:
                    logger.debug("Unicode decode error: %s", err)
                    continue
                except Exception as exc:
                    logger.debug("Caught exception while receiving data: %s", exc)
                    self.terminate_connection(sock, "an exception occurred.")
                    reads.remove(sock)
                    broken_connections.append(sock)
                    continue

                if message == '':
                    self.terminate_connection(sock, "no data was read. (Client closed connection)")
                    broken_connections.append(sock)
                else:
                    logger.debug("Received some data from %s: %s", sock.getpeername(), message.rstrip('\r\n'))
                    self.read_queues[sock].put(message)

        return broken_connections

    def process_data(self):
        pass

    def send_writes(self, writes):
        for sock in writes:
            try:
                message = self.write_queues[sock].get_nowait()
            except queue.Empty:
                pass
            else:
                logger.debug("Sending to %s: %s", sock.getpeername(), message)
                sock.send(message.encode())

    def handle_exceptions(self, exceptions):
        for sock in exceptions:
            self.terminate_connection(sock, "an exception occurred.")

    def accept_new_connection(self, sock):
        connection, client_address = sock.accept()
        logger.info("New connection from %s", client_address)
        connection.setblocking(0)
        self.clients.append(connection)
        self.read_queues[connection] = queue.Queue()
        self.write_queues[connection] = queue.Queue()
        if self.welcome_message:
            self.write_queues[connection].put(self.welcome_message)
        return connection

    def terminate_connection(self, sock, reason=None):
        message = "Terminating connection from (%s:%s)" % sock.getpeername()
        if reason:
            logger.info("%s because %s", message, reason)
        else:
            logger.info("%s. No reason given.", message)
        
        self.clients.remove(sock)
        del self.read_queues[sock]
        del self.write_queues[sock]
        
        sock.close()
        del sock

    def shutdown(self):
        for sock in self.clients:
            self.terminate_connection(sock, "the server is shutting down.")
                
        logger.info("Shutdown successfully.")
