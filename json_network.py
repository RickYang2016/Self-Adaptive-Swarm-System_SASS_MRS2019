#!/usr/bin/env python3

# Author: Zhiwei Luo

from socket import *
import json
import threading

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

    def initSocket(self):
        self.socketUdp = socket(AF_INET, SOCK_DGRAM)
        self.myIPAddr = gethostbyname(gethostname())
        network = self.myIPAddr.split('.')[0:3];network.append('255')
        self.broadcastAddr = '.'.join(network)
        self.socketUdp.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socketUdp.bind(('', self.udpPort))
        self.setBroadcastEnable()

    def setBroadcastEnable(self):
        self.socketUdp.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    def setBlocking(self, block):
        self.socketUdp.setBlocking(block)

    def setTimeout(self, seconds):
        self.socketUdp.settimeout(seconds)

    def retrieveData(self):
        if len(self.bufferList) > 0:
            recvData = self.bufferList[0]
            self.bufferList = self.bufferList[1:]
            return json.loads(recvData.decode('utf-8'))
        else:
            return None

    def examineLatestData(self):
        if len(self.bufferList) > 0:
            recvData = self.bufferList[0]
            return json.loads(recvData.decode('utf-8'))
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
            self.socketUdp.sendto(json.dumps(str), (self.broadcastAddr, self.udpPort))
        except Exception as e:
            print('Send Data Failed!')
            raise e
