'''
Just runs the chat server.
'''
from server import chatserver as cs

serv = cs.ChatServer()
serv.serve_forever()
