'''
Description: load dataset
version: 
Author: WZN1ng
Date: 2022-01-14 19:44:22
LastEditors: WZN1ng
LastEditTime: 2022-02-13 11:46:26
'''

import pandas as pd
import numpy as np
import os


class DataLoader():
    def __init__(self, args, clientId):
        self.args = args
        self.fileRoot = args.dataRoot
        self.seed = args.randomSeed
        self.files = os.listdir(self.fileRoot)
        self.numOfFiles = len(self.files)
        self.sigmaObs = args.sigmaObs
        np.random.seed(self.seed + clientId)
    
    def loadData(self, nodeIdx, noise=True):
        if nodeIdx < self.numOfFiles:
            print("Load ", self.files[nodeIdx])
            data = pd.read_csv(os.path.join(self.fileRoot, self.files[nodeIdx]))
            if noise:
                length = data.shape[0]
                xNoise = np.random.normal(loc=0, scale=self.sigmaObs, size=length)
                yNoise = np.random.normal(loc=0, scale=self.sigmaObs, size=length)
                data["Local_X"] += xNoise
                data["Local_Y"] += yNoise
            return data
        else:
            return pd.DataFrame([])
        
    def getCarId(self, nodeIdx):
        return self.files[nodeIdx]
        