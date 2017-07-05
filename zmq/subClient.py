#coding=utf-8  
''''' 
客户端：SUB订阅模式
'''  
import sys
import zmq
import time

#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")

print sys.argv

filter = sys.argv[1] if len(sys.argv) > 1 else "send"
print filter

#此处设置过滤条件，只有以 zip_filter 开头的消息才会被接收

# !important 必须设置，才能接受到消息
socket.setsockopt(zmq.SUBSCRIBE, filter)
poller = zmq.Poller()
poller.register(socket,zmq.POLLIN)

while(True):
    print("receiving")
    sockets = dict(poller.poll(1000))
    if len(sockets)>0:
        if socket in sockets:
            res= socket.recv()    
            print("recv:%s" % res)
    #time.sleep(3)


