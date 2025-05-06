import numpy as np

def Reward(robot, a, goal, obs):
    R = -0.05
    Terminal = False
    
    # boundary
    if (robot['x'] <= 5) or (robot['x'] >= 295) or (robot['y'] <= 5) or (robot['y'] >= 295):
        Terminal = True
        R = -1 * 10
    # obstacle
    elif np.sqrt((robot['x'] - obs['x'])**2 + (robot['y'] - obs['y'])**2) < 10:
        Terminal = True
        R = -10
    # goal
    elif np.sqrt((robot['x'] - goal['x'])**2 + (robot['y'] - goal['y'])**2) < 10:
        Terminal = True
        R = 10
    
    return R, Terminal