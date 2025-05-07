#!/usr/bin/env python3
import numpy as np
from q_learning import Q_learning
from reward import reward
from object import Robot, Obstacle, Goal
from laser import laser
from plot_map import draw_map
import matplotlib.pyplot as plt
import copy

Episode = 20

goal = Goal(150, 250)
obs = Obstacle(150, 150, 30)
robot0 = Robot(150, 50, np.pi/2, 0)
W = np.ones(6)
dt = 0.1
CoverMODE = 2
M = 1
m = 0  # Python uses 0-based indexing
Eff_robot = 1

index = 0  # Python uses 0-based indexing
fig, ax = plt.subplots(figsize=(6, 6))  # 建立一次即可
plt.ion()  # 開啟互動模式，才能即時更新圖形

for Epi in range(Episode):
    Terminal = False
    robot_t_1 = copy.copy(robot0)
    a = 0  # Python uses 0-based indexing for actions
    
    print(f'Episode={Epi+1}')  # Python is 0-based but we display 1-based like MATLAB
    while not Terminal:
        robot_t = robot_t_1
        robot_t.move(a)
        R, Terminal = reward(robot_t, a, obs, goal)
        
        # Assuming GetLaser is implemented elsewhere
        laser_data = laser(robot_t, obs)
        
        robot_t_1 = copy.copy(robot_t)
        a, Wt, J = Q_learning(a, W, robot_t, goal, laser_data, R, Terminal)
        
        draw_map(robot_t, obs, ax) 
        W = Wt
        # print(W)