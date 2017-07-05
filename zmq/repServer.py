#coding=utf-8
"""服务端，问答模式"""

import zmq
from random import randrange
import time

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    print 'serving running'
    message = socket.recv()  
    print 'received request: ' ,message  
      
    time.sleep(1)  
    if message == 'hello':  
        socket.send('World')  
    else:  
        socket.send('success') 