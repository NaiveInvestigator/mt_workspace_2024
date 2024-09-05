#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion, Pose, Twist, Vector3

class ImuToOdomConverter:
    def __init__(self):
        rospy.init_node('imu2odom', anonymous=True)

        # Define the publishers and subscribers
        self.imu_sub = rospy.Subscriber('/imu/data', Imu, self.imu_callback)
        self.odom_pub = rospy.Publisher('/odometry/filtered', Odometry, queue_size=10)

        # Initialize Odometry message
        self.odom_msg = Odometry()

    def imu_callback(self, imu_msg):
        # Extract relevant data from Imu message and populate Odometry message
        imu_msg.header.frame_id = "odom"
        self.odom_msg.header = imu_msg.header
        self.odom_msg.child_frame_id = "base_link"

        # Populate pose information
        self.odom_msg.pose.pose = Pose()
        self.odom_msg.pose.pose.orientation = imu_msg.orientation

        # Populate twist information
        self.odom_msg.twist.twist = Twist()
        self.odom_msg.twist.twist.angular = imu_msg.angular_velocity
        self.odom_msg.twist.twist.linear = Vector3()  # Assuming linear velocity is not available in the Imu message

        # Publish the Odometry message
        self.odom_pub.publish(self.odom_msg)

if __name__ == '__main__':
    try:
        imu_to_odom_converter = ImuToOdomConverter()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
