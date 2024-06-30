#! /usr/bin/env python3
import rospy
from vectornav.msg import Ins 
from std_msgs.msg import String

lat = 0.0
lon = 0.0
current_yaw = 0.0

rospy.init_node("testies")

def ins_callback(msg):
    global current_yaw, lat, lon
    current_yaw = msg.yaw
    lat = msg.latitude
    lon = msg.longitude

def smth_callback(msg):
    global lat, lon, current_yaw
    whatever = msg.data
    if whatever == "a":
        print(current_yaw, lat, lon)
    else:
        print(whatever)

vectornav_sub = rospy.Subscriber("/vectornav/INS", Ins, ins_callback)
smth_sub = rospy.Subscriber("/smth", String, smth_callback)
rospy.spin()