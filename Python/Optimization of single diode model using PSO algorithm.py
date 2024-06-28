# -*- coding: utf-8 -*-
"""Team22_PSO.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uGC95vDQKyVphRm-W6L6LzR-ri0I_ZgS

import library
"""

import numpy as np
from numpy import random
import math
import matplotlib.pyplot as plt

"""Define the single-diode model equation"""

def I_c(x, v, I):
    I_ph = x[0]
    I_SD = x[1]
    a = x[2]
    R_s = x[3]
    R_sh = x[4]
    V_t = 0.026369  # Thermal voltage (approx. 26 mV at room temperature)
    I_c = I_ph - (I_SD * (np.exp((v+I*R_s)/(a*V_t))-1)) - ((v+I*R_s)/R_sh)
    return I_c

"""Define the function for plotting

"""

#Define the function for plotting cost history
def plot_history(best_history,history,num_particles,b):
    start = b[0]
    end = b[1]
    iterations    = range(b[0],b[1]+1,1)

    for i in range(num_particles):
        plt.plot  (iterations, history[i][b[0]-1:b[1]], 'r',linewidth=1)
    plt.title ('Swarm Cost')
    plt.ylabel('Cost')
    plt.xlabel('Iteration')

    plt.figure()

    plt.plot  (iterations, best_history[b[0]-1:b[1]], 'b',linewidth=1.5,label = 'Global Best')
    plt.title ('Global Best Cost')
    plt.ylabel('Cost')
    plt.xlabel('Iteration')

    plt.figure()

def print_result(best_particle, best_error, history, best_history, n_iter, num_particles):
    print("Optimized Parameters:")
    print("Iph:", best_particle[0])
    print("I0:", best_particle[1])
    print("Rs:", best_particle[3])
    print("Rsh:", best_particle[4])
    print("n:", best_particle[2])
    print("Optimized Error:", best_error)
    if(n_iter == -1):
        n_iter = max_iterations
    print("Number of iterations for convergence: ", n_iter)
    print("Error at convergence: ",best_history[n_iter-1])

"""Define the cost function to be minimized (root mean squared error)"""

def objective_f(x):
 v = [0.2545 , 0.2924 , 0.3269 , 0.3585 , 0.3873 , 0.4137]
 i_exp = [0.7555 , 0.7540 , 0.7505 , 0.7465 , 0.7385 , 0.7280]
 sum=0
 for i in range(0,len(v)):
     objective = ((i_exp[i])-(I_c(x, v[i], i_exp[i])))**2
     sum = sum +objective
 cost = math.sqrt(sum/len(v))
 return cost

"""PSO Algorithm"""

def pso(num_particles,max_iterations,bounds,w,c1,c2,epsilon,ref_error):
 best_history = []
 history = []
 for i in range(num_particles):
    history.append([])
 # Initialize the particles and their velocities
 particles = np.zeros((num_particles, len(bounds)))
 velocities = np.zeros((num_particles, len(bounds)))
 for i in range(num_particles):
        for j in range(len(bounds)):
            particles[i, j] = random.uniform(bounds[j][0], bounds[j][1])
 best_particle = particles[0]
 best_particle_error = np.inf
 global_best = particles[0]
 global_best_error =  np.inf
 past_best_error = np.inf
 num_iter = -1
 for t in range(max_iterations):
 # Evaluate each particle's fitness
        for i in range(num_particles):
            fitness = objective_f(particles[i])
            history[i].append(fitness)
            if fitness < best_particle_error:
                best_particle = particles[i]
                best_particle_error = fitness
            if fitness < global_best_error:
                global_best = particles[i]
                global_best_error = fitness
        best_history.append(global_best_error)
# Update the particle velocities and positions
        for i in range(num_particles):
            for j in range(len(bounds)):
                r1 = random.uniform(0,1)
                r2 = random.uniform(0,1)
                velocities[i, j] = w * velocities[i, j] + c1* r1 * (best_particle[j] - particles[i, j]) + c2 * r2 * (global_best[j] - particles[i, j])
                particles[i, j] = particles[i, j] + velocities[i, j]
                if particles[i, j] < bounds[j][0]:
                    particles[i, j] = bounds[j][0]
                if particles[i, j] > bounds[j][1]:
                    particles[i, j] = bounds[j][1]
        if(num_iter == -1):
            if ((global_best_error < ref_error)and(abs(global_best_error-past_best_error)< epsilon)):
                num_iter = t
            else:
                past_best_error = global_best_error
 return global_best, global_best_error, history, best_history, num_iter

#constant parameters
bounds = [(0.00, 1.00), (0.00, 0.500), (1.00, 2.00), (0.010, 0.500), (0.001, 100.00)]
max_iterations = 4000
max_error = 1.0e-5
ref_error = 0.00715

#the inputs
num_particles = 50
w =  0.1  #inertia
c1 = 0.8 #personal best
c2 = 1 #global best

best_particle, best_error, history, best_history, n_iter = pso(num_particles, max_iterations,bounds,w,c1,c2
                                         ,max_error,ref_error)

print_result(best_particle, best_error, history, best_history, n_iter, num_particles)

b = [1,n_iter]
plot_history(best_history,history,num_particles,b)

#increased inertia *10
#the inputs
num_particles = 50
w =  1  #inertia
c1 = 0.8 #personal best
c2 = 1.7 #global best

best_particle, best_error, history, best_history, n_iter = pso(num_particles, max_iterations,bounds,w,c1,c2
                                         ,max_error,ref_error)

print_result(best_particle, best_error, history, best_history, n_iter, num_particles)

b = [1,50]
plot_history(best_history,history,num_particles,b)

#increased personal *10
#the inputs
num_particles = 50
w =  0.1  #inertia
c1 = 8 #personal best
c2 = 1.7 #global best

best_particle, best_error, history, best_history, n_iter = pso(num_particles, max_iterations,bounds,w,c1,c2
                                         ,max_error,ref_error)

print_result(best_particle, best_error, history, best_history, n_iter, num_particles)

b = [1,25]
plot_history(best_history,history,num_particles,b)

#increased global *3
#the inputs
num_particles = 50
w =  0.1  #inertia
c1 = 0.8 #personal best
c2 = 3 #global best

best_particle, best_error, history, best_history, n_iter = pso(num_particles, max_iterations,bounds,w,c1,c2
                                         ,max_error,ref_error)

print_result(best_particle, best_error, history, best_history, n_iter, num_particles)

b = [1,25]
plot_history(best_history,history,num_particles,b)

#increased number of particles *2
#the inputs
num_particles = 100
w =  0.2  #inertia
c1 = 0.75 #personal best
c2 = 0.95 #global best

best_particle, best_error, history, best_history, n_iter = pso(num_particles, max_iterations,bounds,w,c1,c2
                                         ,max_error,ref_error)

print_result(best_particle, best_error, history, best_history, n_iter, num_particles)

b = [1,50]
plot_history(best_history,history,num_particles,b)

#closest to ref
#the inputs
num_particles = 100
w =  0.2  #inertia
c1 = 0.75 #personal best
c2 = 0.95 #global best

best_particle, best_error, history, best_history, n_iter = pso(num_particles, max_iterations,bounds,w,c1,c2
                                         ,max_error,ref_error)

print_result(best_particle, best_error, history, best_history, n_iter, num_particles)

b = [1,50]
plot_history(best_history,history,num_particles,b)

#least cost
#the inputs
num_particles = 50
w =  0.1  #inertia
c1 = 0.8  #personal best
c2 = 1.7  #global best

best_particle, best_error, history, best_history, n_iter = pso(num_particles,max_iterations,bounds
                                                               ,w,c1,c2,max_error,ref_error)

print_result(best_particle, best_error, history, best_history, n_iter, num_particles)

b = [1,100]
plot_history(best_history,history,num_particles,b)