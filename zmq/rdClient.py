#coding=utf-8  
''''' 

'''  
import zmq  

#  Prepare our context and sockets  
context = zmq.Context()  
socket = context.socket(zmq.REQ)  
#这一次，我们不连接REP，而是连接ROUTER，多个REP连接一个ROUTER  
socket.connect("tcp://localhost:5559")  

#  发送问题给ROUTER  
for request in range(1,11):  
    socket.send(b"Hello")  
    message = socket.recv()  
    print("Received reply %s [%s]" % (request, message))  
socket.close()  
context.term()  