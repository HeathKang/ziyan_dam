#!/usr/bin/env python
# coding:utf8
#author: wangqiankun@lashou-inc.com


import zmq
#调用zmq相关类方法,邦定端口
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://*:10001')



while True:
    #循环接受客户端发来的消息
    msg = socket.recv()
    print "Msg info:%s" %msg
    #向客户端服务器发端需要执行的命令
    cmd_info = raw_input("client cmd info:").strip()
    socket.send(cmd_info)

socket.close()
