#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import NavSatFix
from time import sleep

lat, lon = 0.0, 0.0

def gps_callback(msg):
    global lat, lon
    lat = msg.latitude
    lon = msg.longitude


gps_sub = rospy.Subscriber("/navsat/fix", NavSatFix, gps_callback)
