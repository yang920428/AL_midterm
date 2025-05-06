#!/usr/bin/env python3

import numpy as np

class Robot:
    def __init__(self, x, y, t, w):
        self.x = x
        self.y = y
        self.t = t  # 朝向角度（度）
        self.w = w

    def move_forward(self, step=1):
        # 依朝向移動
        theta = np.radians(self.angle())
        self.x += step * np.sin(theta)
        self.y += step * np.cos(theta)
        
    def turn_around(self, step=1, a = 0):
        if a == 2:
            self.w = 0
        elif a == 1:
            self.w = -15
        elif a == 3:
            self.w = 15
        elif a == 0:
            self.w = -30
        else:
            self.w = 30
        self.t += step * self.w 
    
    def angle(self):
        if self.t >= 180:
            self.t = self.t - 360
        elif self.y <= -181:
            self.t = self.t + 360
        return self.t

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