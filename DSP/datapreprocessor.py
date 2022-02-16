'''
Description: data preprocess function
version: 
Author: WZN1ng
Date: 2022-01-14 14:44:38
LastEditors: WZN1ng
LastEditTime: 2022-02-13 11:46:34
'''

import os
import pandas as pd

USEFULSERIES = ["Vehicle_ID", "Frame_ID", "Total_Frames", "Local_X", "Local_Y", "v_Vel", "v_Acc"]

class DataPreProcessor():
    def __init__(self, numOfNodes):
        self.numOfNodes = numOfNodes
        self.fileRoot = "datasets"
        self.fileName = "AllData.csv"
        self.path = os.path.join(self.fileRoot, self.fileName)
        self.sortedFileName = "SortedData.csv"
        self.sortedPath = os.path.join(self.fileRoot, self.sortedFileName)
        
    def SortAndSaveAllData(self):
        self.data = pd.read_csv(self.path)[USEFULSERIES].sort_values(by="Total_Frames", ascending=False)
        self.data.to_csv(self.sortedPath)
        
    def DivideSortAndSaveData(self):
        self.data = pd.read_csv(self.sortedPath)
        distributedRoot = os.path.join(self.fileRoot, 'distributed')
        if not os.path.exists(distributedRoot):
            os.makedirs(distributedRoot)
        vehicleID, totalFrames = self.data.loc[0, "Vehicle_ID"], self.data.loc[0, "Total_Frames"]
        idx, start, row = 0, 0, 0
        while idx < self.numOfNodes:
            if (self.data.loc[row, "Vehicle_ID"] != vehicleID or\
                self.data.loc[row, "Total_Frames"] != totalFrames):
                dataTmp = self.data.loc[start:row-1, :]
                dataTmp = dataTmp.sort_values(by="Frame_ID")
                path = os.path.join(distributedRoot, str(vehicleID) + ".csv")
                dataTmp.to_csv(path)
                start = row
                vehicleID = self.data.loc[row, "Vehicle_ID"]
                totalFrames = self.data.loc[row, "Total_Frames"]
                idx += 1
            row += 1

    def test(self):
        pass
    
if __name__ == '__main__':
    d = DataPreProcessor(7)
    d.SortAndSaveAllData()
    d.DivideSortAndSaveData()