#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import tf
import time
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32
import math


def orientation_callback(msg):
    global quaternion
    quaternion = msg.orientation

    roll, pitch, yaw = tf.transformations.euler_from_quaternion([
        quaternion.x, 
        quaternion.y, 
        quaternion.z, 
        quaternion.w
    ])

    yaw_pub.publish(yaw * (180 / math.pi) + 180)

def yaw_callback(msg):
    global current_yaw
    current_yaw = msg.data 

def avoid_obstacle(target_yaw):
    yaw_tolerance = 5

    rospy.loginfo("Turning to avoid obstacle")
    while not (target_yaw - yaw_tolerance <= current_yaw <= target_yaw + yaw_tolerance):
        vel_msg = Twist()
        vel_msg.angular.z = 0.5
        cmd_vel_pub.publish(vel_msg)

    end_time = time.time() + 5.0
    rospy.loginfo("Moving forward to avoid obstacle")
    while time.time() <= end_time:
        vel_msg = Twist()
        vel_msg.linear.x = 1.0
        cmd_vel_pub.publish(vel_msg)
    
    rospy.loginfo("Turning back to original yaw")
    target_yaw = target_yaw - 90.0
    while not (target_yaw - yaw_tolerance <= current_yaw <= target_yaw + yaw_tolerance):
        vel_msg = Twist()
        vel_msg.angular.z = -0.5
        cmd_vel_pub.publish(vel_msg)


def spiral_motion():
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10) 

    vel_msg = Twist()

    linear_velocity = 0.1
    angular_velocity = 0.5
    linear_acceleration = 0.01  

    start_time = time.time()

    while not rospy.is_shutdown():
        current_time = time.time()
        elapsed_time = current_time - start_time
        vel_msg.linear.x = linear_velocity + linear_acceleration * elapsed_time
        vel_msg.angular.z = angular_velocity

        velocity_publisher.publish(vel_msg)

        rate.sleep()

if __name__ == '__main__':

    rospy.init_node('spiral_motion_node')

    rospy.Subscriber('/imu/data', Imu, orientation_callback)
    yaw_pub = rospy.Publisher('/yaw_angle', Float32, queue_size=10)
    cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/yaw_angle', Float32, yaw_callback)

    while yaw_pub.get_num_connections() == 0:
        rospy.sleep(0.1)  

    # avoid_obstacle(current_yaw + 90.0)

    rospy.spin()