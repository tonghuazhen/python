#coding=utf-8  
''''' 
你无法连续向服务器发送数据，必须发送一次，接收一次 
REQ和REP模式中，客户端必须先发起请求 

'''  
import zmq  
import time

context = zmq.Context()  
print 'connect to hello world server'  
socket =  context.socket(zmq.REQ)  
socket.connect('tcp://localhost:5555')  

while True:  
    print 'send ','...'  
    socket.send('hello')  
    message = socket.recv()  
    print 'received reply ','[',message,']'  
    time.sleep(3)