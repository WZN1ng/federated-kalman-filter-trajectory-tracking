'''
Description: start, manage, monitor and end threads
version: 
Author: WZN1ng
Date: 2022-01-13 14:18:23
LastEditors: WZN1ng
LastEditTime: 2022-02-13 10:17:50
'''

from client import Client
from server import Server
import threading
import time

class Runner:
    def __init__(self, args):
        self.args = args
        self.frame = args.frame
        self.numberOfThreads = args.node
        self.alg = args.alg
        self.updateInterval = args.updateInterval
        self.currIdx = args.updateInterval
        
        self.clients = []
        self.prepareList = []
        self.threads = []
        self.msgs = {}
        self.threadLock = threading.Lock()
        self.barrier = threading.Barrier(self.numberOfThreads - 1)
        self.finish = threading.Barrier(2)
        self.server = None
        self.clientIdxs = list(range(self.numberOfThreads))
        self.serverIdx = -1
        if self.frame == 'cs':
            self.serverIdx = args.serverIdx
            if self.serverIdx in self.clientIdxs:
                self.clientIdxs.remove(self.serverIdx)
            self._allocateServerNode(self.serverIdx)
        self._allocateClientNodes(self.clientIdxs)
        
        self.finish.wait()
        # self.server.drawTrajectory()
        self.error = self.server.getError()
    
    def getError(self):
        return self.error
    
    def waitForAllNodesPreparation(self, clientId):
        self.threadLock.acquire()
        if clientId not in self.prepareList:
            self.prepareList.append(clientId)
        self.threadLock.release()
        
        if len(self.prepareList) == self.numberOfThreads:
            print("All Nodes initialed.")
            self.prepareList.clear()
            self.threads.clear()
            self._runAllClientNodes()
            
    def waitForAllClientsFinish(self, clientId):
        self.threadLock.acquire()
        if clientId not in self.prepareList:
            self.prepareList.append(clientId)
        self.threadLock.release()
        
        if len(self.prepareList) == self.numberOfThreads - 1:
            print("Task finished.")
            # res = self.server.getLocations()
            self.prepareList.clear()
            self.threads.clear()
            self.finish.wait()
            
    def collectMsgFromClientToServer(self, clientId, msg, idx):
        self.threadLock.acquire()
        if clientId not in self.prepareList and idx == self.currIdx:
            self.prepareList.append(clientId)
            self.msgs[clientId] = msg
        
        if len(self.prepareList) == self.numberOfThreads - 1:
            if self.currIdx % 100 == 0:
                print("All reply received. Barrier Release. (Steps:{})".format(self.currIdx))
            self.server.dataFusion(self.msgs, self.currIdx)
            self.prepareList.clear()
            self.msgs.clear()
            self.threads.clear()
            self.currIdx += self.updateInterval
        self.threadLock.release()
            
    def _runAllClientNodes(self):
        for client in self.clients:
            newThread = threading.Thread(target=client.run, daemon=True, \
                name="client"+str(client.clientId))
            self.threads.append(newThread)
            newThread.start()
    
    def _allocateClientNodes(self, clientIdxs):
        for idx in clientIdxs:
            newClient = Client(self.args, idx, self.barrier, self.threadLock, self)
            self.clients.append(newClient)
            newThread = threading.Thread(target=newClient.loadData, daemon=True, name="client"+str(idx))
            self.threads.append(newThread)
            newThread.start()
        
    def _allocateServerNode(self, serverIdx):
        newServer = Server(self.args, serverIdx, self)
        self.server = newServer
        self.server.prepare()
        # newThread = threading.Thread(target=newServer.prepare, daemon=True, name="server"+str(serverIdx))
        # self.threads.append(newThread)
        # newThread.start()