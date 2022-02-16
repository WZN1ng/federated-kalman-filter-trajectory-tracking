'''
Description: main program
version: 1.0
Author: WZN1ng
Date: 2022-01-13 13:51:25
LastEditors: WZN1ng
LastEditTime: 2022-02-13 10:41:13
'''

from cProfile import label
from arguments import getArgs, AddClientServerArgs, AddFullyDecentralizedArgs, AddKalmanArgs
from runner import Runner
from matplotlib import pyplot as plt
import os

def getAllArgs():
    args = getArgs()
    try:
        if args.frame == 'cs':
            args = AddClientServerArgs(args)
        elif args.frame == 'dec':
            args = AddFullyDecentralizedArgs(args)
        else:
            raise ValueError('Unknown frame.')
        if args.alg == 'kalman':
            args = AddKalmanArgs(args)
        else:
            raise ValueError('Unknown algorithm.')
    except ValueError as v:
        print("Terminated.", repr(v))
    return args

def drawErrorOfDiffIntervals(args):
    interval = [1, 2, 5, 10, 20 ,50]
    error = {}
    for inter in interval:
        print("Interval = ", inter)
        args.updateInterval = inter
        runner = Runner(args)
        error[inter] = runner.getError()
    plt.figure(2)
    files = os.listdir(args.dataRoot)
    title = "Error of Different Intervals (Car {})".format(files[args.dataIdx].split('.')[0])
    plt.title(title)
    plt.xlabel("Steps")
    plt.ylabel("Error")
    for key, value in error.items():
        plt.plot(value[0], value[1])
    plt.legend(loc='best', labels=["interval = " + str(inter) for inter in interval])
    plt.savefig(os.path.join("res", title))
    plt.show()
    

if __name__ == "__main__":
    args = getAllArgs()
    # runner = Runner(args)
    drawErrorOfDiffIntervals(args)
    