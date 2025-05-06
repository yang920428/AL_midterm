#!/usr/bin/env python3
import numpy as np
import random
from feature import features

def Q_learning(a, W, robot, goal, laser, R, terminal):
    alpha = 5e-4
    gamma = 0.9
    epsilon = 0.1
    num_actions = 5

    f_current = features(robot, goal, laser, a)  # +1 to match MATLAB's 1-based action indexing
    Q_current = np.dot(W.T, f_current)

    if terminal:
        Q_target = R
    else:
        Q_next = np.zeros(num_actions)
        for a_next in range(num_actions):
            f_next = features(robot, goal, laser, a_next)  # +1 for MATLAB compatibility
            Q_next[a_next] = np.dot(W.T, f_next)
        Q_target = R + gamma * np.max(Q_next)

    TD_error = Q_target - Q_current
    J = TD_error**2

    Wt = W + alpha * TD_error * f_current

    if random.random() < epsilon:
        opt_a = random.randint(0, num_actions-1)  # 0-based in Python
    else:
        Q_eval = np.zeros(num_actions)
        for a_candidate in range(num_actions):
            f = features(robot, goal, laser, a_candidate)  # +1 for MATLAB compatibility
            Q_eval[a_candidate] = np.dot(Wt.T, f)
        opt_a = np.argmax(Q_eval)

    return opt_a, Wt, J