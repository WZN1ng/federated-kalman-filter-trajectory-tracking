'''
Description: server node
version: 
Author: WZN1ng
Date: 2022-01-13 14:22:05
LastEditors: WZN1ng
LastEditTime: 2022-02-13 10:24:12
'''
from dataloader import DataLoader
from matplotlib import pyplot as plt
import numpy as np
import time
import os
import math

class Server():
    def __init__(self, args, serverId, runner):
        self.args = args
        self.serverId = serverId
        self.runner = runner
        self.mode = args.serverMode
        self.obsSize = args.obsSize
        self.maxSteps = args.maxSteps
        self.timeSleep = args.timeSleep
        self.updateInterval = args.updateInterval
        self.clientWeights = args.clientWeights
        # print(self.clientWeights)
        
    def prepare(self):
        self.locs = np.zeros((self.obsSize, self.maxSteps//self.updateInterval - 1))
        print("Server {} Initialized.".format(self.serverId))
        self.runner.waitForAllNodesPreparation(self.serverId)
        
    def dataFusion(self, msg, idx):
        t = idx // self.updateInterval - 1
        x, y = 0, 0
        # print(msg)
        for key, value in msg.items():
            x += self.clientWeights[key] * value[0]
            y += self.clientWeights[key] * value[1]
            self.locs[:, t] = np.array([x, y])
    
    def getLocations(self):
        return self.locs
    
    def drawTrajectory(self):
        realLoc = self._loadDataWithoutNoise()
        plt.figure(1)
        title = "Trajectory of Car " + self.d.getCarId(self.args.dataIdx).split('.')[0]
        plt.title(title)
        plt.xlabel("Local_X")
        plt.ylabel("Local_Y")
        plt.scatter(realLoc.loc[1:self.maxSteps:self.updateInterval, "Local_X"],\
            realLoc.loc[1:self.maxSteps:self.updateInterval, "Local_Y"], \
            marker='.', c='b')
        plt.scatter(self.locs[0, :-1], self.locs[1, :-1], marker='x', c='r')
        plt.legend(loc='best', labels=["Real Trajectories", "Filter Tracking"])
        plt.savefig(os.path.join("res", title + ".png"))
        plt.show()
        
    def getError(self):
        realLoc = self._loadDataWithoutNoise()
        n = self.maxSteps//self.updateInterval
        error = np.zeros(n)
        # print(realLoc.loc[0, "Local_X"], realLoc.loc[1, "Local_X"], realLoc.loc[2, "Local_X"], self.locs[0, 0], self.locs[0, 1])
        for i in range(n - 1):
            error[i] = math.sqrt((realLoc.loc[1 + self.updateInterval * i, "Local_X"] - self.locs[0, i]) ** 2 + \
                (realLoc.loc[1 + self.updateInterval * i, "Local_Y"] - self.locs[1, i]) ** 2)
        return [[self.updateInterval * (i + 1) for i in range(n)], error]
        # plt.figure(2)
        # plt.plot([self.updateInterval * (i + 1) for i in range(n)], error)
        # plt.show()
    
    def _loadDataWithoutNoise(self):
        self.d = DataLoader(self.args, self.serverId)
        while True:
            data = self.d.loadData(self.args.dataIdx, True)
            if data.shape[0]:
                break
            else:
                print("Server fails to load data. Try again {}s later.".format(self.timeSleep))
                time.sleep(self.timeSleep)
        return data