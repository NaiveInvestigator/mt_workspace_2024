#! /usr/bin/env python3

import rospy
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import String
from math import degrees

rospy.init_node("gps_node")

lat, lon = 0, 0

def gps_callback(msg):
    global lat, lon
    lat = msg.latitude
    lon = msg.longitude
    print(f"{round(lat, 8)} {round(lon, 8)}")

sub = rospy.Subscriber("/gps/info", NavSatFix, gps_callback)
pub = rospy.Publisher("/gps_", String, queue_size=10)


r = rospy.Rate(1)
while not rospy.is_shutdown():
    pub.publish(f"{round(lat, 6)} {round(lon, 6)}")
    r.sleep()