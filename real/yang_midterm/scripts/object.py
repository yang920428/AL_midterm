#!/usr/bin/env python3

import numpy as np

class Robot:
    def __init__(self, x, y, t, w):
        self.x = x
        self.y = y
        self.t = t  # 朝向角度（度）
        self.w = w
        
    def move(self, a = 0):
        dt = 0.1
        if a == 2:
            self.w = 0
        elif a == 1:
            self.w = np.deg2rad(-15)
        elif a == 3:
            self.w = np.deg2rad(15)
        elif a == 0:
            self.w = np.deg2rad(-30)
        elif a == 4:
            self.w = np.deg2rad(30)

        # theta = np.radians(self.angle())
        self.x=self.x+15 *np.cos(self.t)*dt
        self.y=self.y+15 *np.sin(self.t)*dt
        self.t=self.t+self.w*dt

class Obstacle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
    
    def is_hit(self, px, py):
        return (px - self.x)**2 + (py - self.y)**2 <= self.r**2
    
class Goal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def arrived_goal(self, px, py):
        return (px - self.x)**2 + (py - self.y)**2 <= 100