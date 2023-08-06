import matplotlib.pyplot as plt
import os
import numpy as np
import random


# This class is structly acting as a struct for plot data


def plot_single_comparison(self, x1, y1, x2, y2, xL, yL, test_name, class_name, save_dir=None, replace=False):
    # plot the data
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(x1, y1, color='tab:blue')
    ax.plot(x2, y2, color='tab:orange', linestyle=":")
    ax.set_ylabel(yL)
    ax.set_xlabel(xL)
    plt.legend(["Preconditioned", "Standard"])
    joinDir = self.figDir if save_dir is None else save_dir
    save_name = os.path.join(joinDir, "{:s}-vs-{:s}-{:s}-{:s}".format(xL, yL, test_name, class_name))
    if not replace:
        ctr = 1
        while os.path.exists(save_name+"-{:d}.pdf".format(ctr)):
            ctr += 1
        plt.savefig(save_name+"-{:d}.pdf".format(ctr))
    else:
        plt.savefig(save_name+".pdf")
    plt.close()


def plot_multi_comparison(self, x1, y1, x2, y2, xL, yL, test_name, class_name, leg_labs=[]):
    # plot the data
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    rows, cols = np.shape(y1)
    for i in range(cols):
        color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
        ax.plot(x1, y1[:, i], color=color[0])
        ax.plot(x2, y2[:, i], color=color[0], linestyle=":")
    # plt.show()
    ax.set_ylabel(yL)
    ax.set_xlabel(xL)
    if leg_labs:
        plt.legend(leg_labs)
    save_name = "./figures/{:s}-vs-{:s}-{:s}-{:s}".format(xL, yL, test_name, class_name)
    ctr = 1
    while os.path.exists(save_name+"-{:d}.pdf".format(ctr)):
        ctr += 1
    plt.savefig(save_name+"-{:d}.pdf".format(ctr))
    plt.close()


def plot_species(self, reactor, x1, y1, x2, y2, xL, yL, test_name, class_name):
    dname = str.join("-", (class_name, test_name, "species-plots"))
    dname = os.path.join(self.figDir, dname)
    rows, cols = np.shape(y1)
    if not os.path.isdir(dname):
        os.mkdir(dname)
    for i in range(cols):
        if (np.mean(y1[:, i]) > self.net1.rtol):
            name = reactor.component_name(i+1)
            plot_single_comparison(self, x1, y1[:, i], x2,  y2[:, i], xL, "MF-{:s}".format(name), test_name+"-{:s}".format(name), class_name, save_dir=dname, replace=True)


def plotter(self, func_name):
    self.plot_single_comparison(self.p_data.steps, self.p_data.iters, self.s_data.steps, self.s_data.iters, "steps", "iters", func_name, self.__class__.__name__, replace=True)
    self.plot_single_comparison(self.p_data.steps, self.p_data.itersLin, self.s_data.steps, self.s_data.itersLin, "steps", "itersLin", func_name, self.__class__.__name__, replace=True)
    # self.plot_single_comparison(self.p_data.times, self.p_data.iters, self.s_data.times, self.s_data.iters, "times", "iters", func_name, self.__class__.__name__, replace=True)
    # self.plot_single_comparison(self.p_data.times, self.p_data.itersLin, self.s_data.times, self.s_data.itersLin, "times", "itersLin", func_name, self.__class__.__name__, replace=True)
    # if 'steady_state' not in func_name:
    #     self.plot_single_comparison(self.p_data.times, self.p_data.T, self.s_data.times, self.s_data.T, "times", "temperature", func_name, self.__class__.__name__, replace=True)
    #     self.plot_species(self.r1, self.p_data.times, self.p_data.Y, self.s_data.times, self.s_data.Y, "times", "mass-fraction", func_name, self.__class__.__name__)

