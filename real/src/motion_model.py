import numpy as np

def motion_model(robot_t_1, a, dt):
    VW = {'v': 15}
    
    # Convert action to angular velocity (rad/s)
    if a == 3:  # Note: Python uses 0-based indexing for actions (0-4)
        VW['w'] = -30 * np.pi / 180
    elif a == 1:
        VW['w'] = -15 * np.pi / 180
    elif a == 0:
        VW['w'] = 0
    elif a == 2:
        VW['w'] = 15 * np.pi / 180
    elif a == 4:
        VW['w'] = 30 * np.pi / 180
    
    # Update robot state
    robot_t = {
        'x': robot_t_1['x'] + VW['v'] * np.cos(robot_t_1['t']) * dt,
        'y': robot_t_1['y'] + VW['v'] * np.sin(robot_t_1['t']) * dt,
        't': robot_t_1['t'] + VW['w'] * dt
    }
    
    return robot_t