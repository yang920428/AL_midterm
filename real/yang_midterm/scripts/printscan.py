#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
import math

counter = 0
file = open("laser.txt", "w")

def callback_timer(event):
    global counter, file
    counter += 1
    rospy.loginfo("sample file called : %d\t times", counter)
    if counter > 300:
        file.close()
        rospy.signal_shutdown("Reached 300 samples")

def scan_callback(scan):
    global file
    for i in range(len(scan.ranges)):
        degree = (scan.angle_min + scan.angle_increment * i) * 180.0 / math.pi
        if scan.ranges[i] != 0.0 and not math.isinf(scan.ranges[i]):
            file.write(f"{degree:4.1f} {scan.ranges[i]:5.3f}\n")

def listener():
    rospy.init_node('listener', anonymous=True)
    
    # 每0.1秒執行一次 callback_timer
    rospy.Timer(rospy.Duration(0.1), callback_timer)
    
    # 訂閱 /scan 主題
    rospy.Subscriber("/scan", LaserScan, scan_callback)

    rospy.spin()

if __name__ == '__main__':
    listener()

