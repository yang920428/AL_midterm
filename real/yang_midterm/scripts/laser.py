#!/usr/bin/env python3

import numpy as np

def laser(robot, obs):
    angles = [-30, -15, 0, 15, 30]
    max_range = 100
    result = []

    for angle in angles:
        theta = robot.t + np.deg2rad(angle)
        x0, y0 = robot.x, robot.y
        dist = max_range

        for r in range(1, max_range + 1):
            x = x0 + r * np.sin(theta)
            y = y0 + r * np.cos(theta)

            if x < 0 or x > 300 or y < 0 or y > 300:
                dist = r
                break

            elif obs.is_hit(x, y):
                dist = r
                break
            else:
                continue
            break

        result.append(dist)
    # print(result)

    return result
