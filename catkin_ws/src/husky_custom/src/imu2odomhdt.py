#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion, Pose, Twist, Vector3
from sbg_driver.msg import SbgGpsHdt, SbgGpsPos
import geonav_transform.geonav_conversions as gc
from tf.transformations import quaternion_from_euler
import math

lat_org, lon_org =  23.761655672, 90.36131751799999
lat, lon = 0.0, 0.0

class ImuToOdomConverter:
    def __init__(self):
        rospy.init_node('imu2odomhdt', anonymous=True)

        self.nav_sat_sub = rospy.Subscriber("/sbg/gps_pos", SbgGpsPos, self.gps_callback)
        self.imu_hdt_sub = rospy.Subscriber('/sbg/gps_hdt', SbgGpsHdt, self.gps_hdt_callback)
        self.imu_sub = rospy.Subscriber('/imu/data', Imu, self.imu_callback)
        self.odom_pub = rospy.Publisher('/odometry/filtered', Odometry, queue_size=10)

        self.odom_msg = Odometry()

    def gps_callback(self, msg):
        global lat, lon
        lat, lon = gc.ll2xy(float(msg.latitude), float(msg.longitude), lat_org, lon_org)
        # lat, lon = float(msg.latitude), float(msg.longitude)
        # lat, lon = gc.ll2xy(23.761649464999998, 90.361280386, lat_org, lon_org)

    def gps_hdt_callback(self, msg):
        quat = quaternion_from_euler(0, 0, msg.true_heading * math.pi / 180)

        self.odom_msg.pose.pose.orientation.x = quat[0]
        self.odom_msg.pose.pose.orientation.y = quat[1]
        self.odom_msg.pose.pose.orientation.z = quat[2]
        self.odom_msg.pose.pose.orientation.w = quat[3]

        self.odom_pub.publish(self.odom_msg)

    def imu_callback(self, imu_msg):
        global lat, lon
        imu_msg.header.frame_id = "odom"
        self.odom_msg.header = imu_msg.header
        self.odom_msg.child_frame_id = "base_link"

        self.odom_msg.pose.pose = Pose()

        self.odom_msg.pose.pose.position.x = lat
        self.odom_msg.pose.pose.position.y = lon

        self.odom_msg.pose.pose.orientation = imu_msg.orientation
 
        self.odom_msg.twist.twist = Twist()
        self.odom_msg.twist.twist.angular = imu_msg.angular_velocity
        self.odom_msg.twist.twist.linear = Vector3()  

if __name__ == '__main__':
    try:
        imu_to_odom_converter = ImuToOdomConverter()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
