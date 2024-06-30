#! /usr/bin/env python3

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from time import sleep

rospy.init_node("rover")

rover = rospy.Publisher("cmd_vel", Twist, queue_size=10)

forward = Twist().linear.x = 1
#forward = Twist().linear.x = 1
backward = Twist().linear.x = -1
left = Twist().angular.z = 0.5
right = Twist().angular.z = -0.5
stop = Twist()

def move_callback(msg):
    vel = Twist()
    stop = Twist()
    keys = msg.data
    if keys == "w":
        vel.linear.x = 1
        vel.angular.z = 0
    if keys == "a":
        vel.linear.x = 0
        vel.angular.z = 20
    if keys == "s":
        vel.linear.x = -1
        vel.angular.z = 0
    if keys == "d":
        vel.linear.x  = 0
        vel.angular.z = -20
    if keys == "-":
        vel.linear.x = 0
        vel.angular.z = 0

    rover.publish(vel)
    sleep(0.05)
    rover.publish(stop)  
    print(keys)


listener = rospy.Subscriber("/rover_control", String, move_callback)
rospy.spin()