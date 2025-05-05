import matplotlib.pyplot as plt
import numpy as np

def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 2:
                continue  # 忽略不合格式的行
            try:
                angle = float(parts[0])
                distance = float(parts[1])
                data.append((angle, distance))
            except ValueError:
                continue  # 忽略不能轉為 float 的行
    return data

def split_cycles(data):
    """
    將資料依照角度由小變大（遇到角度變小就代表新一圈）來分段。
    """
    cycles = []
    current_cycle = []
    last_angle = -1

    for angle, distance in data:
        if angle < last_angle:
            # 進入新一圈
            if current_cycle:
                cycles.append(current_cycle)
                current_cycle = []
        current_cycle.append((angle, distance))
        last_angle = angle

    if current_cycle:
        cycles.append(current_cycle)
    return cycles

def plot_cycles(cycles):
    for i, cycle in enumerate(cycles):
        angles = [np.deg2rad(p[0]) for p in cycle]
        distances = [p[1] for p in cycle]

        plt.figure()
        ax = plt.subplot(111, polar=True)
        ax.plot(angles, distances)
        ax.set_title(f'Cycle {i+1}')
        plt.show()

# 主程式區
filename = "../data/laser.txt"  # 替換為你的檔案路徑
data = read_data(filename)
cycles = split_cycles(data)
plot_cycles(cycles)
