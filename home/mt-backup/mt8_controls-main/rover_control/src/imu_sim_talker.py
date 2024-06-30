#! /usr/bin/env python3

import rospy
from sensor_msgs.msg import Imu
from std_msgs.msg import String
from tf.transformations import euler_from_quaternion
from math import degrees

yaw = 0

def get_rotation (msg):
    global roll, pitch, yaw
    orientation_q = msg.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    roll, pitch, yaw = euler_from_quaternion(orientation_list)
    print(round(degrees(yaw), 3))

rospy.init_node('imu')

sub = rospy.Subscriber ('/imu_raw', Imu, get_rotation)
pub = rospy.Publisher("/imu", String, queue_size=10)

r = rospy.Rate(1)
while not rospy.is_shutdown():
    pub.publish(round(degrees(yaw), 3))
    r.sleep()