# -*- coding:utf-8 -*-

import zmq

import time

import commands

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://127.0.0.1:10001')


def execut_cmd(cmd):
    s,v = commands.getstatusoutput(cmd)
    return v

result = 'dir'

while True:
    #获取当前时间
    now_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

    socket.send("now time info:[%s] request execution command:'\n',%s"%(now_time,result))
    recov_msg = socket.recv()
    #调用execut_cmd函数,执行服务器发过来的命令
    result = execut_cmd(recov_msg)
    print recov_msg,'\n',result,
    time.sleep(1)
    #print "now time info:%s cmd status:[%s],result:[%s]" %(now_time,s,v)
    continue

socket.close()