from __future__ import division
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from drawnow import drawnow, figure
import matplotlib.animation as animation
import sys
from PyQt4 import QtGui

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

import timeit
'''This program demostrate a 1D FDTD simulatino'''

# Define initial constants
eps_0 = 8.854187817E-12     # permittivity of free space
mu_0 = 4*np.pi*1E-7     # permeability of free space
c = 1/np.sqrt(mu_0*eps_0)

# Define probelm geometry and parameters
domain_size = 1     # 1D problem space length in meters
dx = 1E-3       # cell size in meters
dt = 3E-12      # duration of time step in seconds
number_of_time_steps = 2000      # number of iterations
nx = np.round(domain_size/dx)       # number of cells in 1d problem space
source_position = 0.5       # position of the current source jz

# Initialize field and material arrays
ceze = np.zeros(int(nx+1))
cezhy = np.zeros(int(nx+1))
cezj = np.zeros(int(nx+1))
ez = np.zeros(int(nx+1))
jz = np.zeros(int(nx+1))
eps_r_z = np.ones(int(nx+1))     # free space
sigma_e_z = np.zeros(int(nx+1))      # free space
chyh = np.zeros(int(nx+1))
chyez = np.zeros(int(nx+1))
chym = np.zeros(int(nx+1))
hy = np.zeros(int(nx+1))
my = np.zeros(int(nx+1))
mu_r_y = np.ones(nx)        # free space
sigma_m_y = np.zeros(nx)    # free space


#Calcualte FDTD updating coefficients
ceze = [(2*eps_r_z[i]*eps_0 - dt*sigma_e_z[i])/(2*eps_r_z[i]*eps_0 + dt*sigma_e_z[i])
        for i in range(int(nx+1))]
cezhy = [(2*dt/dx)/(2*eps_r_z[i]*eps_0 + dt*sigma_e_z[i]) for i in range(int(nx+1))]
cezj = [(-2*dt)/(2*eps_r_z[i]*eps_0 + dt*sigma_e_z[i]) for i in range(int(nx+1))]
chyh = [(2*mu_r_y[i]*mu_0 - dt*sigma_m_y[i])/(2*mu_r_y[i]*mu_0 + dt*sigma_m_y[i])
        for i in range(int(nx))]
chyez = [(2*dt/dx)/(2*mu_r_y[i]*mu_0 + dt*sigma_m_y[i]) for i in range(int(nx))]
chym = [(-2*dt)/(2*mu_r_y[i]*mu_0 + dt*sigma_m_y[i])  for i in range(int(nx))]

# Define the Gaussian source waveform
time = range(int(number_of_time_steps))
time = [time[i]*dt for i in range(int(number_of_time_steps))]
jz_waveform = [np.exp(-((time[i] - 2E-10)/(5E-11))**2) for i in 
                range(int(number_of_time_steps))]
source_position_index = np.round(nx*source_position/domain_size)+1




# Subroutine to initialize plotting
#initialize_plotting_parameters

ez_positions = range(int(nx+1))
ez_positions = [ez_positions[i]*dx for i in range(int(nx+1))]
hy_positions = range(int(nx))
hy_positions = [dx*(0.5 + hy_positions[i]) for i in range(int(nx))]
v = [[0, -0.1, -0.1], [0, -0.1, 0.1], [0, 0.1, 0.1], [0, 0.1, -0.1],
     [1, -0.1, -0.1], [1, -0.1, 0.1], [1, 0.1, 0.1], [1, 0.1, -0.1]]
f = [[1,2,3,4],[5,6,7,8]]
    
#fig = plt.figure()
#ax = Axes3D(fig)
#ax.plot(xs=ez_positions,ys=[ez[i]*0 for i in range(int(nx+1))],zs=ez, color='red')
#ax.plot(xs=hy_positions,ys=[hy[i]*377 for i in range(int(nx))],
#                zs=[hy[i]*0 for i in range(int(nx))], color='blue')
#ax.set_xlabel('x [m]')
#ax.set_ylabel('[A/m]')
#ax.set_zlabel('[V/m]')
#plt.show()

#def function_to_draw_figure():
#    fig = plt.figure()
#    ax = Axes3D(fig)
#    ax.plot(xs=ez_positions,ys=[ez[i]*0 for i in range(int(nx+1))],zs=ez, color='red')
#    ax.plot(xs=hy_positions,ys=[hy[i]*377 for i in range(int(nx))],
#                    zs=[hy[i]*0 for i in range(int(nx))], color='blue')
#    ax.set_xlabel('x [m]')
#    ax.set_ylabel('[A/m]')
#    ax.set_zlabel('[V/m]')
##    def update_img():
##        ax.plot(xs=ez_positions,ys=[ez[i]*0 for i in range(int(nx+1))],zs=ez, color='red')
##        ax.plot(xs=hy_positions,ys=[hy[i]*377 for i in range(int(nx))],
##                    zs=[hy[i]*0 for i in range(int(nx))], color='blue')
#    #plt.imshow([xs,ys,ez], interpolation='nearest')
#    plt.grid(True)
#    plt.show()

#figure(1)
#function_to_draw_figure(plt)


class Monitor(FigureCanvas):
    def __init__(self):
        self.fig = plt.figure()
        self.ax = Axes3D(self.fig)
        
        FigureCanvas.__init__(self, self.fig)
#        self.xs = ez_positions
#        self.ys = [ez[i]*0 for i in range(int(nx+1))]
#        self.zs = ez


#        self.line = self.ax.plot(self.x,self.y)
        self.p = 0
        self.line = self.ax.plot(xs=ez_positions,ys=[ez[i]*0 for i in range(int(nx+1))],
                                    zs=ez, color='red')
        self.line = self.ax.plot(xs=hy_positions,ys=[hy[i]*377 for i in range(int(nx))],
                                    zs=[hy[i]*0 for i in range(int(nx))], color='blue')

        self.fig.canvas.draw()

        self.timer = self.startTimer(1)
        


    def timerEvent(self, evt):
        # update the height of the bars, one liner is easier
        self.p += 1
        
        if self.p == 1999:
            sys.exit()
        global jz, hy, ez
        jz[source_position_index] = jz_waveform[self.p]
        #Update magentic field
        
        hy = [chyh[i]*hy[i] + chyez[i]*(ez[i+1]-ez[i]) + chym[i]*my[i] for i in range(int(nx))]
        # Update electric field    
        for i in range(1,int(nx)):
            ez[i] = ceze[i]*ez[i] + cezhy[i]*(hy[i]-hy[i-1]) + cezj[i]*jz[i] 
        ez[0] = 0 # Apply PEC boundary conditionat x = 0m
        ez[int(nx)] = 0 
        self.ax.cla()
        self.line = self.ax.plot(xs=ez_positions,ys=[ez[i]*0 for i in range(int(nx+1))],
                                    zs=ez, color='red')
        self.line = self.ax.plot(xs=hy_positions,ys=[hy[i]*377 for i in range(int(nx))],
                                    zs=[hy[i]*0 for i in range(int(nx))], color='blue')
        
        self.fig.canvas.draw()
        


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = Monitor()
    w.setWindowTitle("Convergence")
    w.show()
    sys.exit(app.exec_())




# FDTD loop

#figure(1)
#for time_step in range(int(number_of_time_steps)):
#    # Update jz for the current time step    
#    jz[source_position_index] = jz_waveform[time_step]
#    #Update magentic field
#    hy = [chyh[i]*hy[i] + chyez[i]*(ez[i+1]-ez[i]) + chym[i]*my[i] for i in range(int(nx))]
#    # Update electric field    
#    for i in range(1,int(nx)):
#        ez[i] = ceze[i]*ez[i] + cezhy[i]*(hy[i]-hy[i-1]) + cezj[i]*jz[i] 
#    ez[0] = 0 # Apply PEC boundary conditionat x = 0m
#    ez[int(nx)] = 0 # Apply PEC boundary conditionat x = 1m
#    
##    drawnow(function_to_draw_figure)


























