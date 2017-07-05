#coding=utf-8  
''''' 
收到请求后回复world 
'''  
import zmq  

context = zmq.Context()  
socket = context.socket(zmq.REP)  
# REP连接的是DEALER  
socket.connect("tcp://localhost:5560")  

while True:  
    message = socket.recv()  
    print("Received request: %s" % message)  
    socket.send(b"World") 	