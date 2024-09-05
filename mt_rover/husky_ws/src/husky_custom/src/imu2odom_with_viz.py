#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion, Pose, Twist, Vector3
from sbg_driver.msg import SbgGpsPos 
from std_msgs.msg import String
import geonav_transform.geonav_conversions as gc
from tf.transformations import euler_from_quaternion
import math

lat_org, lon_org = -35.2339193, 92.726221
lat, lon = 0.0, 0.0
class ImuToOdomConverter:
    def __init__(self):
        rospy.init_node('imu2odom', anonymous=True)

        # Define the publishers and subscribers
        self.nav_sat_sub = rospy.Subscriber("/sbg/gps_pos", SbgGpsPos, self.gps_callback)
        self.imu_sub = rospy.Subscriber('/imu/data', Imu, self.imu_callback)
        self.odom_pub = rospy.Publisher('/odometry/filtered', Odometry, queue_size=10)

        self.quat2euler = rospy.Publisher('/quat2euler', String, queue_size=10)

        # Initialize Odometry message
        self.odom_msg = Odometry()

    def gps_callback(self, msg):
        global lat, lon
        lat, lon = gc.ll2xy(float(msg.latitude), float(msg.longitude), lat_org, lon_org)
        # lat, lon = gc.ll2xy(23.761649464999998, 90.361280386, lat_org, lon_org)
        # lat = float(msg.latitude) 
        # lon = float(msg.longitude)

    def imu_callback(self, imu_msg):
        global lat, lon
        # Extract relevant data from Imu message and populate Odometry message
        imu_msg.header.frame_id = "odom"
        self.odom_msg.header = imu_msg.header
        self.odom_msg.child_frame_id = "base_link"

        # Populate pose information
        self.odom_msg.pose.pose = Pose()

        self.odom_msg.pose.pose.position.x = lat
        self.odom_msg.pose.pose.position.y = lon

        self.odom_msg.pose.pose.orientation = imu_msg.orientation

        euler = euler_from_quaternion([ imu_msg.orientation.x, imu_msg.orientation.y, imu_msg.orientation.z, imu_msg.orientation.w ])
        # rospy.loginfo(euler)
        euler = euler[2] * (180) / math.pi + 180
        self.quat2euler.publish(str(euler))
        # self.odom_msg.pose.pose.orientation.x *= -1.0

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

