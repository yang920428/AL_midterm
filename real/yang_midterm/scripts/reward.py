#!/usr/bin/env python3

from utils import collision_detect
from laser import laser

# def reward(robot, action, obs, goal):
    
#     if collision_detect(robot, obs):
#         return -100, 1
#     if goal.arrived_goal(robot.x, robot.y):
#         return 100, 1
#     laser_length = laser(robot, obs)[action]
#     goal_distance = ((robot.x-goal.x)**2 + (robot.x-goal.x)**2)**(1/2)
#     return laser_length/10 + goal_distance/292*10, 0

def reward(robot, action, obs, goal):
    
    if collision_detect(robot, obs):
        return -10, 1
    if goal.arrived_goal(robot.x, robot.y):
        return 10, 1
    # laser_length = laser(robot, obs)[action]
    # goal_distance = ((robot.x-goal.x)**2 + (robot.x-goal.x)**2)**(1/2)
    return -0.05, 0