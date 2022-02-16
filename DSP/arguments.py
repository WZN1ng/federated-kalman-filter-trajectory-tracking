'''
Description: argument related functions
version: 
Author: WZN1ng
Date: 2022-01-13 13:53:41
LastEditors: WZN1ng
LastEditTime: 2022-02-13 10:56:50
'''

import argparse

def getArgs():
    parser = argparse.ArgumentParser()
    
    # arguments 
    parser.add_argument('--alg', type=str, default='kalman', help='the algorithm used(kalman, lms, rls)')
    parser.add_argument('--frame', type=str, default='cs', help='cs:client-server dec:fully decentralized')
    parser.add_argument('--node', type=int, default=11, help='number of client nodes')
    parser.add_argument('--dataIdx', type=int, default=6, help='the index of the dataset')
    parser.add_argument('--randomSeed', type=int, default=19990227, help='random seed of noise')
    parser.add_argument('--dataRoot', type=str, default="datasets/distributed", help='the file root of datasets')
    
    args = parser.parse_args()
    return args

def AddClientServerArgs(args):
    args.serverIdx = args.node - 1 # use the last node as server, 0-node-2 as clients
    args.synchronize = True
    args.updateInterval = 5
    args.timeSleep = 1
    args.clientWeights = [1 / (args.node - 1) for _ in range(args.node - 1)]
    
    args.serverMode = 1
        # 1: only fusion the location results
    return args

def AddFullyDecentralizedArgs(args):
    return args

def AddKalmanArgs(args):
    args.stateSize = 4
    args.obsSize = 2
    args.maxSteps = 1000
    args.dt = 0.1
    args.sigmaState = 1
    args.sigmaObs = 1
    
    return args