import matplotlib.pyplot as plt
import ruamel_yaml, os, random, inspect, importlib
import numpy as np
from mpi4py import MPI
import cantera_adaptive_testing.mechanisms as mechanisms


def printYamlVariables(yamlFileName):
    data = getYamlData(yamlFileName)
    key1 = list(data.keys())[0]
    subdata = data[key1]
    varList = list(subdata.keys())
    print(varList)
    return varList


def getYamlData(yamlFileName):
    data = dict()
    yaml = ruamel_yaml.YAML()
    f = open(yamlFileName, 'r')
    previous = yaml.load(f)
    data.update(previous)
    return data


def plotYamlVariables(xVar, yVar, yamlFileName, save=True):
    # get yaml data
    data = getYamlData(yamlFileName)
    precon = list()
    standard = list()
    for key in data.keys():
        if "Preconditioned" in key:
            precon.append((data[key][xVar], data[key][yVar]))
        else:
            standard.append((data[key][xVar], data[key][yVar]))
    # formatting data to plot
    arr = np.sort(np.array(precon), axis=0)
    xp, yp = zip(*arr)
    arr = np.sort(np.array(standard), axis=0)
    xs, ys = zip(*arr)
    # plot the data
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(xp, yp, color='tab:blue')
    ax.plot(xs, ys, color='tab:orange')
    ax.set_ylabel(yVar)
    ax.set_xlabel(xVar)
    plt.legend(["Preconditioned", "Standard"])
    if save:
        plt.savefig("./figures/"+xVar+"-vs-"+yVar+".pdf")
    else:
        plt.show()
