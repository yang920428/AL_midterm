#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from object import Robot, Obstacle
from utils import collision_detect
from laser import laser
import numpy as np

# 這裡用內建的雷射函數來畫出五條線
def plot_laser(robot, obs, ax):
    distances = laser(robot, obs)
    angles = [-30, -15, 0, 15, 30]

    for d, a in zip(distances, angles):
        theta = np.radians(robot.t + a)
        x0, y0 = robot.x, robot.y
        x1 = x0 + d * np.sin(theta)
        y1 = y0 + d * np.cos(theta)
        ax.plot([x0, x1], [y0, y1], color='blue')

# 畫整張地圖
def draw_map(robot, obs, ax):
    ax.clear()
    ax.set_xlim(0, 300)
    ax.set_ylim(0, 300)
    ax.set_aspect('equal')

    # 畫障礙物與終點
    ax.add_patch(plt.Circle((obs.x, obs.y), obs.r, color='black'))
    ax.plot(150, 250, 'rx', markersize=10, markeredgewidth=2)

    # 畫機器人
    ax.add_patch(plt.Circle((robot.x, robot.y), 5, color='blue'))

    # 畫雷射
    plot_laser(robot, obs, ax)

    # 網格與標題
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.set_xticks(range(0, 301, 50))
    ax.set_yticks(range(0, 301, 50))
    ax.set_title("Robot Animation")

    plt.pause(0.01)



# 主動畫流程
def run_simulation():
    robot = Robot(150, 50, 90, -1)
    obs = Obstacle(150,150,20)

    fig, ax = plt.subplots(figsize=(6, 6))

    def update(frame):
        if not collision_detect(robot, obs):
            robot.turn_around(step=1)
            robot.move_forward(step=2)  # 每次移動2單位
        draw_map(robot, obs, ax)

    ani = animation.FuncAnimation(fig, update, frames=200, interval=50, repeat=False)
    plt.show()

if __name__ == "__main__":
    run_simulation()
