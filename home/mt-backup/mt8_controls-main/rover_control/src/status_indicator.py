#! /usr/bin/env python3

import rospy
from std_msgs.msg import String
import serial

rospy.init_node("status")
lights = serial.Serial("/dev/ttyACM1", 9600, timeout=10)
rate = rospy.Rate(5)

def status_callback(msg):
    if msg.data in ["r", "g", "b"]:
        lights.write(bytes(msg.data, "utf-8"))
        rospy.loginfo(msg.data)

status = rospy.Subscriber("/status_indicator", String, status_callback)

rate.sleep()
rospy.spin()
