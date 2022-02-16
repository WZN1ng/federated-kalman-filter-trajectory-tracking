'''
Description: client node
version: 
Author: WZN1ng
Date: 2022-01-13 14:21:56
LastEditors: WZN1ng
LastEditTime: 2022-02-12 16:20:34
'''

import time

from matplotlib.pyplot import bar
from dataloader import DataLoader
from alg.kalman import KalmanFilter

class Client():
    def __init__(self, args, clientId, barrier, lock, runner):
        self.args = args
        self.clientId = clientId
        self.maxSteps = args.maxSteps
        self.timeSleep = args.timeSleep
        self.runner = runner
        self.synchronize = args.synchronize
        self.updateInterval = args.updateInterval
        self.barrier = barrier
        self.lock = lock
        self.index = 0
        if args.alg == 'kalman':
            self.filter = KalmanFilter(args)
        
    def loadData(self):
        d = DataLoader(self.args, self.clientId)
        while True:
            self.data = d.loadData(self.args.dataIdx)
            if self.data.shape[0]:
                break
            else:
                print("Client {} fails to load data. Try again {}s later.".format(self.clientId, self.timeSleep))
                time.sleep(self.timeSleep)
        print("Client {} initialized.".format(self.clientId), end='\n')
        self.filter.setInitState([self.data.loc[0, "Local_X"], 0, self.data.loc[0, "Local_Y"], 0])
        self.index += 1
        self.runner.waitForAllNodesPreparation(self.clientId)
        
    def run(self):
        for i in range(self.maxSteps):
            newObs = [self.data.loc[self.index, "Local_X"], self.data.loc[self.index, "Local_Y"]]
            if not self.filter.step(newObs):
                print("Filter step failed.")
                break
            self.index += 1
            if i % self.updateInterval == 0 and i != 0:
                # self.lock.acquire()     # abusing threadlock to make output elegant ^.^
                # print("Client {} connect server. (Steps:{})".format(self.clientId, i), end='\n')
                # self.lock.release()
                self.runner.collectMsgFromClientToServer(self.clientId, self.filter.getCurrLocation(), i)
                self.barrier.wait()
        self.runner.waitForAllClientsFinish(self.clientId)