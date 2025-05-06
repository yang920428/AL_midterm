#!/usr/bin/env python3

import math

def collision_detect(robot, obs):
    dx = robot.x - obs.x
    dy = robot.y - obs.y
    if dx**2 + dy**2 <= 10**2: # 撞障礙
        return 1
    elif robot.x <= 5 or robot.y <= 5 or robot.x >= 295 or robot.y >= 295: #撞牆
        return 1
    else: return 0
