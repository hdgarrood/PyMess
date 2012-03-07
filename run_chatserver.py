'''
Created on 4 Mar 2012

@author: Harry
'''
from server import chatserver as cs

serv = cs.ChatServer()
serv.serve_forever()
