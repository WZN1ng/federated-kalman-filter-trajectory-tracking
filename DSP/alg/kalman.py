'''
Description: kalman filter algorithm
version: 
Author: WZN1ng
Date: 2022-01-15 14:50:20
LastEditors: WZN1ng
LastEditTime: 2022-02-13 11:46:04
'''
import numpy as np

class KalmanFilter():
    def __init__(self, args):
        self.stateSize = args.stateSize
        self.maxSteps = args.maxSteps
        self.obsSize = args.obsSize
        self.dt = args.dt
        self.sigmaState = args.sigmaState
        self.sigmaObs = args.sigmaObs
        self.Kf = np.mat([[1, self.dt, 0, 0], [0, 1, 0, 0], [0, 0, 1, self.dt], [0, 0, 0, 1]])
        self.Cf = np.mat([[1, 0, 0, 0], [0, 0, 1, 0]])
        self.covStateNoise = np.diag([self.sigmaState for _ in range(self.stateSize)])
        self.covObsNoise = np.diag([self.sigmaObs for _ in range(self.obsSize)])
        self.I = np.diag([1 for _ in range(self.stateSize)])
        self.reset()
    
    def reset(self):
        self.statePredict = np.zeros((self.stateSize, self.maxSteps, 1))
        self.stateCorrect = np.zeros((self.stateSize, self.maxSteps + 1, 1))
        self.errorPredict = np.zeros((self.stateSize, self.stateSize, self.maxSteps))
        self.errorCorrect = np.zeros((self.stateSize, self.stateSize, self.maxSteps + 1))
        self.kalmanGain = np.zeros((self.stateSize, self.obsSize, self.maxSteps))
        self.currentStep = 0
        
    def setInitState(self, initState):
        self.stateCorrect[:, 0, :] = np.array(initState).reshape((self.stateSize, 1))
        # print(self.stateCorrect[:, 0, :].shape)
        
    def step(self, obs):
        if self.currentStep >= self.maxSteps:
            return False
        
        obs = np.array(obs).reshape((self.obsSize, 1))
        self.statePredict[:, self.currentStep, :] = self.Kf * self.stateCorrect[:, self.currentStep, :]
        self.errorPredict[:, :, self.currentStep] = self.Kf * self.errorCorrect[:, :, self.currentStep] * self.Kf.T\
                + self.covStateNoise
        self.kalmanGain[:, :, self.currentStep] = self.errorPredict[:, :, self.currentStep] * self.Cf.T * \
                np.linalg.inv(self.Cf * self.errorPredict[:, :, self.currentStep] * self.Cf.T + self.covObsNoise)
        self.stateCorrect[:, self.currentStep + 1, :] = self.statePredict[:, self.currentStep, :] + \
                self.kalmanGain[:, :, self.currentStep] * (obs - self.Cf * self.statePredict[:, self.currentStep, :])
        self.errorCorrect[:, :, self.currentStep + 1] = self.errorPredict[:, :, self.currentStep] - self.Kf * \
                self.kalmanGain[:, :, self.currentStep] * self.Cf * self.errorPredict[:, :, self.currentStep]
        self.currentStep += 1
        # print(self.statePredict[:, self.currentStep])
        # print(self.errorPredict[:, :, self.currentStep])
        # print(self.kalmanGain[:, :, self.currentStep])
        # print(self.stateCorrect[:, self.currentStep, :])
        # print(self.errorCorrect[:, :, self.currentStep + 1])
        
        return True
    
    def getCurrLocation(self):
        locaCorrect = [self.stateCorrect[0, self.currentStep, 0], self.stateCorrect[2, self.currentStep, 0]]
        return locaCorrect
        
if __name__ == '__main__':
    k = KalmanFilter()
    k.setInitState([30, 5, 30, -5])
    k.step([31, 29])