#! /usr/bin/env python3

import serial
import rospy
from std_msgs.msg import String
from time import sleep

rospy.init_node("imu_talker")

imu_port = "/dev/ttyACM0"

imu = serial.Serial(imu_port, 9600, timeout=1)
imu_node = rospy.Publisher("/imu", String, queue_size=10)

"""
#this is for the autonomous node
yaw = None
def callback(msg):
    global yaw
    yaw = int(msg.data)
"""

while not rospy.is_shutdown():
    yaw = imu.readline().decode().strip()
    imu_node.publish(yaw)
