#!/usr/bin/env python3

# Author: Zhiwei Luo

from socket import *
import _pickle as pickle
import threading

class TaskLoader:
    taskList = []

    def __init__(self):
        pass

    def addTask(self, task):
        self.taskList.append(task)

    def getTaskCount(self):
        return len(taskList)

    def start(self):
        for task in self.taskList:
            task.run()

class Task:
    strategy = None
    def __init__(self, strategy):
        self.strategy = strategy

    def run(self):
        if self.strategy != None:
            while not self.strategy.checkFinished():
                self.strategy.go()

class Strategy:
    def checkFinished(self):
        return True

    def go(self):
        pass

class NetworkInterface:
    udpPort = 6666
    socketUdp = None
    isBufferFull = False
    contextMouse = None
    receiveBuffer = None
    receiveAddr = None
    broadcastAddr = None
    myIPAddr = None
    bufferList = []
    threadReceive = None

    def __init__(self, context=None, port=6666):
        self.udpPort = port
        self.contextMouse = context

    def initSocket(self, port=udpPort):
        self.socketUdp = socket(AF_INET, SOCK_DGRAM)
        self.myIPAddr = gethostbyname(gethostname())
        network = self.myIPAddr.split('.')[0:3];network.append('255')
        self.broadcastAddr = '.'.join(network)
        self.socketUdp.bind(('', self.udpPort))
        self.setBroadcastEnable()

    def setBroadcastEnable(self):
        self.socketUdp.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    def setBlocking(self, block):
        self.socketUdp.setBlocking(block)

    def setTimeout(self, seconds):
        self.socketUdp.settimeout(seconds)

    def receiveData(self):
        #while not self.contextMouse.isEndNetwork:
        try:
            str, addr = self.socketUdp.recvfrom(1000)
            self.bufferList.append((str, addr))
            return (str, addr)
        except:
            print('Receive Data Failed!')
            return None

    def retrieveData(self):
        if len(self.bufferList) > 0:
            recvData = self.bufferList[0]
            self.bufferList = self.bufferList[1:]
            return pickle.loads(recvData)
        else:
            return None

    def receiveDataThread(self):
        #while not self.contextMouse.isEndNetwork:
        while True:
            str, addr = self.socketUdp.recvfrom(1000)
            self.bufferList.append(str)

    def startReceiveThread(self):
        self.threadReceive = threading.Thread(name='receive', target=self.receiveDataThread)
        self.threadReceive.setDaemon(True)
        self.threadReceive.start()

    def sendStringData(self, str):
        try:
            self.socketUdp.sendto(pickle.dumps(str), (self.broadcastAddr, self.udpPort))
        except:
            print('Send Data Failed!')
