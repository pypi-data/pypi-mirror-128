import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib import animation as pltanim


class animate(object):
    def __init__(self,dataset, frames, interval, num = 4, Ne=100, xlim=(-1,1), ylim=(-1,1), circle=False):
        self.df = dataset
        self.frames = frames 
        print(len(dataset), len(self.df))
        self.animation = self.anim(self.df,frames=frames, interval=interval,num = num, Ne=Ne, xlim=xlim, ylim=ylim, circle=circle)

    def anim(self, datas, frames, interval,num = 4, Ne=100, xlim=(-1,1), ylim=(-1,1), circle=False):
        XD = []
        YD = []
        self.num = num
        # self.datas = np.array(datas)
        print('shape is ======', len(datas))
        for i in range(self.num):
            XD.append(datas[i])
            YD.append(datas[i+self.num])
        self.Ne = Ne
        self.frames = frames 
        self.interval = interval
        self.fig = plt.figure('plotpy')
        self.xlim = xlim
        self.ylim = ylim
        self.ax = plt.axes(xlim=self.xlim, ylim=self.ylim)
        self.finarr = 3*(self.Ne)+4
        self.lines = []
        self.circle = circle
        if not self.circle:
            for i in range(self.num):
                self.lines.append(self.ax.plot([], [], lw=3)[0])
        def draw(i):
            for j in range(self.num):
                self.lines[j].set_data(np.array(XD[j])[i],np.array(YD[j])[i])
            return self.lines
        anim = pltanim.FuncAnimation(self.fig, draw, frames=self.frames, interval=self.interval, blit=True)
        return anim
