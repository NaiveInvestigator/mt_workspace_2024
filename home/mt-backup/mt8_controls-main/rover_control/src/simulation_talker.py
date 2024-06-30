#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Vector3

rospy.init_node("simulation_talker")

rospy.Rate(10)

sim_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

def controlCallback(msg: String):
    # Handle w,a,s,d
    l = Twist()
    if msg.data == "w":
        sim_pub.publish(Twist(linear=Vector3(2, 0, 0)))
    elif msg.data == "a":
        sim_pub.publish(Twist(angular=Vector3(0, 0, 1.25)))
    elif msg.data == "s":
        sim_pub.publish(Twist(linear=Vector3(-2, 0, 0)))
    elif msg.data == "d":
        sim_pub.publish(Twist(angular=Vector3(0, 0, -1.25)))
    elif msg.data == "-": # Stop
        sim_pub.publish(Twist(angular=Vector3(0, 0, 0), linear=Vector3(0, 0, 0)))
    

control_pub = rospy.Subscriber("/rover_control", String, controlCallback, queue_size=10)

rospy.spin()
