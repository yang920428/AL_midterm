#!/usr/bin/env python3
import numpy as np

def features(robot, goal, laser, a):
    dist_to_goal = np.sqrt((robot.x- goal.x)**2 + (robot.y - goal.y)**2) / 100
    angle_to_goal = np.arctan2(goal.y - robot.y, goal.x - robot.x) - robot.t
    angle_to_goal = np.arctan2(np.sin(angle_to_goal), np.cos(angle_to_goal))  # Equivalent to wrapToPi
    
    if a == 0:
        idx = 2  # Note: Python uses 0-based indexing, adjusted from MATLAB's 1-based
    elif a == 1:
        idx = 1
    elif a == 2:
        idx = 3
    elif a == 3:
        idx = 0
    else:
        idx = 4
    
    f4 = -angle_to_goal
    if laser[idx] <= 70:
        f4 = angle_to_goal
    
    cover = (laser[idx] / 100 + np.min([idx]) / 100)

    w = 0
    if np.cos(angle_to_goal) > np.cos(np.deg2rad(15)):
        if idx == 2:  # Corresponds to MATLAB idx=3
            w = 1
        else:
            w = 0.2
    elif angle_to_goal > 0:
        if idx >= 3:  # Corresponds to MATLAB idx >=4
            w = 0.7
    else:
        if idx <= 1:  # Corresponds to MATLAB idx <=2
            w = 0.7
    
    return np.array([
        1,
        dist_to_goal,
        angle_to_goal,
        f4,
        w,
        -1/(cover + 0.01)
    ])