# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 12:55:55 2015

@author: Charleseagle
"""

import sys
from PyQt4 import QtGui

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

import numpy as np


class Monitor(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.x = np.linspace(0,5*np.pi,400)
        self.p = 0.0
        self.y = np.sin(self.x+self.p)


        self.line = self.ax.scatter(self.x,self.y)

        self.fig.canvas.draw()

        self.timer = self.startTimer(100)


    def timerEvent(self, evt):
        # update the height of the bars, one liner is easier
        self.p += 1
        self.y = np.sin(self.x+self.p)
        self.ax.cla()
        self.line = self.ax.scatter(self.x,self.y)

        self.fig.canvas.draw()



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = Monitor()
    w.setWindowTitle("Convergence")
    w.show()
    sys.exit(app.exec_())