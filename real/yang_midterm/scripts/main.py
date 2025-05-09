#!/usr/bin/env python3

import numpy as np
from q_learning import Q_learning
from reward import reward
from object import Robot, Obstacle, Goal
from laser import laser
from plot_map import draw_map
import matplotlib.pyplot as plt
import copy

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math
global laser_data

laser_data = [0.0] * 5  # 或用 None 預設都為 0.0 公尺


Episode = 20

goal = Goal(0, 184)
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

# 要讀的角度（度）
desired_degrees = [0, 15, 30, 330, 345]
desired_indices = []

def scan_callback(msg):
    global desired_indices, laser_ready, laser_data

    if not desired_indices:
        # 第一次收到的時候建立索引對應（只做一次）
        angle_min = msg.angle_min  # 單位是 rad
        angle_increment = msg.angle_increment  # 單位是 rad
        num_ranges = len(msg.ranges)

        for deg in desired_degrees:
            rad = math.radians(deg)
            idx = int((rad - angle_min) / angle_increment)
            if 0 <= idx < num_ranges:
                desired_indices.append(idx)

    # 取得五個對應角度的距離資料
    laser_data = [100 * msg.ranges[i] for i in desired_indices]
    # print(laser_data)
    laser_ready = True
    
laser_ready = False
laser_features = []

rospy.init_node('q_learning_controller')
rospy.Subscriber('/scan', LaserScan, scan_callback)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
rate = rospy.Rate(10)  # 每 0.1 秒
# rospy.spin()

lock = False
for Epi in range(Episode):
    if (lock):
        break
    Terminal = False
    robot_t_1 = copy.copy(robot0)
    a = 0  # Python uses 0-based indexing for actions
    print(f'Episode={Epi+1}')  # Python is 0-based but we display 1-based like MATLAB
    while not Terminal and not rospy.is_shutdown():
        if (Terminal == 2):
            lock = True
            break
        if not laser_ready:
            continue
        laser_ready = False
        print("laser:")
        print(laser_data)
        robot_t = robot_t_1
        robot_t.move(a)
        R, Terminal = reward(robot_t, a, laser_data, goal)
        
        twist = Twist()
        if a == 2:
            twist.linear.x = 0.15
        elif a == 1:
            twist.linear.x = 0.15
            twist.angular.z = -0.262
        elif a == 3:
            twist.linear.x = 0.15
            twist.angular.z = 0.262
        elif a == 0:
            twist.linear.x = 0.15
            twist.angular.z = -0.524
        else:
            twist.linear.x = 0.15
            twist.angular.z = 0.524

        twist.linear.x = twist.linear.x * 0.5
        pub.publish(twist)
        
        # print(twist.linear.x)
        # print(twist.angular.z)
        # Assuming GetLaser is implemented elsewhere
        # laser_data = laser(robot_t, obs)
        
        robot_t_1 = copy.copy(robot_t)
        a, Wt, J = Q_learning(a, W, robot_t, goal, laser_data, R, Terminal)
        
        # draw_map(robot_t, obs, ax) 
        W = Wt
        # print(W)
        rate.sleep()
        #