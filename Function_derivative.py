from __future__ import division
import matplotlib.pyplot as plt
import numpy as np

#N_exact= input('number of sample points for exact funciton:')
N_exact = 301
x_exact = np.linspace(0,6*np.pi,N_exact)

f_exact = [np.sin(x_exact[i])*np.exp(-0.3*x_exact[i]) for i in range(0,N_exact)]
f_derivative_exact = [np.cos(x_exact[i])*np.exp(-0.3*x_exact[i]) - 
                        0.3*np.sin(x_exact[i])*np.exp(-0.3*x_exact[i]) for i in range(0,N_exact)]

'''plot exact function'''
#plt.figure(1)
#plt.subplot(221)
plt.figure(1)
plt.plot(x_exact,f_exact, color='red', linestyle = 'solid')
#plt.axis(0,6*np.pi-11,-1,1)
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.savefig('Fig1.jpg')
plt.show()

'''create exact function for pi/5 sampling period and its fnite difference derivatives'''
N_a = 31 # number of points for pi/5 sampling period
x_a = np.linspace(0,6*np.pi,N_a)
f_a = [np.sin(x_a[i])*np.exp(-0.3*x_a[i]) for i in range(N_a)]
f_derivative_a = [np.cos(x_a[i])*np.exp(-0.3*x_a[i]) - 0.3*np.sin(x_a[i])*np.exp(-0.3*x_a[i]) 
        for i in range(0,N_a)]
    
dx_a = np.pi/5
f_derivative_froward_a = np.zeros(N_a)
f_derivative_backward_a = np.zeros(N_a)
f_derivative_central_a = np.zeros(N_a)
for i in range(N_a-1):
    f_derivative_froward_a[i] = (f_a[i+1]-f_a[i])/dx_a
    f_derivative_backward_a[i+1] = (f_a[i+1]-f_a[i])/dx_a
    if i < N_a-2:
        f_derivative_central_a[i+1] = (f_a[i+2]-f_a[i])/(2*dx_a)
    else:
        break

'''creat exact function for pi/10 sampling period and its finite difference derivatives'''
N_b = 61 # number of points for pi/10 sampling period
x_b = np.linspace(0,6*np.pi,N_b)
f_b = [np.sin(x_b[i])*np.exp(-0.3*x_b[i]) for i in range(N_b)]
f_derivative_b = [np.cos(x_b[i])*np.exp(-0.3*x_b[i]) - 0.3*np.sin(x_b[i])*np.exp(-0.3*x_b[i]) 
        for i in range(0,N_b)]
        
dx_b = np.pi/10
f_derivative_froward_b = np.zeros(N_b)
f_derivative_backward_b = np.zeros(N_b)
f_derivative_central_b = np.zeros(N_b)
for i in range(N_b-1):
    f_derivative_froward_b[i] = (f_b[i+1]-f_b[i])/dx_b
    f_derivative_backward_b[i+1] = (f_b[i+1]-f_b[i])/dx_b
    if i < N_b-2:
        f_derivative_central_b[i+1] = (f_b[i+2]-f_b[i])/(2*dx_b)
    else:
        break

'''plot exact derivative of the function and its finite difference derivatives 
using pi/5 sampling period'''

#plt.figure(1)
#plt.subplot(222)
plt.figure(2)
plt.plot(x_exact,f_derivative_exact, 'r-', label='exact')
plt.plot(x_a[0:N_a-2],f_derivative_froward_a[0:N_a-2], 'b--', label='forward')
plt.plot(x_a[1:N_a-1],f_derivative_backward_a[1:N_a-1], 'gs',label='backward')
plt.plot(x_a[1:N_a-2],f_derivative_central_a[1:N_a-2], 'k^', label='central')
plt.xlabel('x')
plt.ylabel('f\'(x)')
plt.title('as delta_x = pi/5, exact derivative and finit difference approximation')
plt.legend(loc=9)
plt.grid(True)
plt.savefig('Fig2.jpg')
plt.show()


'''plot error for finite difference derivatives using pi/5 sampling period'''
error_forward_a =  f_derivative_a - f_derivative_froward_a 
error_backward_a = f_derivative_a - f_derivative_backward_a
error_central_a = f_derivative_a - f_derivative_central_a

#plt.figure(1)
#plt.subplot(223)
plt.figure(3)
plt.plot(x_a[0:N_a-2],error_forward_a[0:N_a-2], 'r--', label='forward_error')
plt.plot(x_a[1:N_a-1],error_backward_a[1:N_a-1], 'bo', label='backward_error')
plt.plot(x_a[1:N_a-2],error_central_a[1:N_a-2], 'k^', label='central_error')
plt.xlabel('x')
plt.ylabel('Error of derivative')
plt.legend(loc=9)
plt.title('as delta_x = pi/5, error compared to the exact derivative')
plt.grid(True)
plt.savefig('Fig3.jpg')
plt.show()


'''plot error for finite difference derivatives using pi/10 sampling period'''
error_forward_b =  f_derivative_b - f_derivative_froward_b 
error_backward_b = f_derivative_b - f_derivative_backward_b
error_central_b = f_derivative_b - f_derivative_central_b

#plt.figure(1)
#plt.subplot(224)
plt.figure(4)
plt.plot(x_b[0:N_b-2],error_forward_b[0:N_b-2], 'r--', label='forward_error')
plt.plot(x_b[1:N_b-1],error_backward_b[1:N_b-1], 'bo', label='backward_error')
plt.plot(x_b[1:N_b-2],error_central_b[1:N_b-2], 'k^', label='central_error')
plt.xlabel('x')
plt.ylabel('Error of derivative')
plt.legend(loc=9)
plt.title('as delta_x = pi/10, error compared to the exact derivative')
plt.grid(True)
plt.savefig('Fig4.jpg')
plt.show()