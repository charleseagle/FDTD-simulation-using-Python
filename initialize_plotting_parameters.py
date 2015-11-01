from __future__ import division
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# subroutine used to initialize 1D plot

def 1Dplot(dx,ez,hy):
    ez_positions = dx*range(int(nx+1))
    hy_positions = dx*(0.5 + range(int(nx)))
    v = [[0, -0.1, -0.1], [0, -0.1, 0.1], [0, 0.1, 0.1], [0, 0.1, -0.1],
     [1, -0.1, -0.1], [1, -0.1, 0.1], [1, 0.1, 0.1], [1, 0.1, -0.1]]
    f = [[1,2,3,4],[5,6,7,8]]
    
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot(ez_positions,[ez[i]*0 for i in range(int(nx+1))],ez, color='red')
    ax.plot(hy_positions,[hy[i]*377 for i in range(int(nx))],
                [hy[i]*0 for i in range(int(nx))], color='blue')
    ax.set_xlabel('x [m]')
    ax.set_ylabel('[A/m]')
    ax.set_zlabel('[V/m]')
    grid(True)
    plt.show()
    


