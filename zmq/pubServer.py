#coding=utf-8
"""服务端，发布模式"""

import zmq
from random import randrange
import time

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

while True:
    for v in range(0,3):
        print "send:%i" % v
        socket.send("send:%i" % v)
    time.sleep(3)
