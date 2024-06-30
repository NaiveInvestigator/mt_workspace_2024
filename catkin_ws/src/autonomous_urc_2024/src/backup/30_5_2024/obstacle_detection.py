#! /usr/bin/env python3

import rospy
from std_msgs.msg import String, Float32
from sensor_msgs.msg import Imu, NavSatFix, Image
from tf import transformations
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from math import radians, cos, sin, asin, sqrt, atan2, degrees
from time import sleep
from sbg_driver.msg import SbgGpsPos, SbgEkfEuler
import numpy as np
import pyrealsense2 as rs
import cv2
from cv_bridge import CvBridge, CvBridgeError

rospy.init_node("obstacle_detection")

def depth_image_callback(data):
    inflation_radius = 250
    obstacle_presence = 0.0

    bridge = CvBridge()
    try:
        # Assuming the depth image is encoded in 16UC1 format
        depth_frame = bridge.imgmsg_to_cv2(data, desired_encoding="16UC1")
    except CvBridgeError as e:
        rospy.logerr("CvBridge Error: {0}".format(e))
        return
    
    depth_frame[depth_frame == 0.0] = 100000.0
    depth_bool = depth_frame < inflation_radius
    
    if depth_bool.any():
        obstacle_presence = 1.0
    else:
        obstacle_presence = 0.0
    obstacle_pub.publish(obstacle_presence)

    depth_bool = depth_bool.astype(np.uint8)
    depth_bool[depth_bool == 1] = 255
    cv2.imshow("Obstacle view", depth_bool)
    cv2.waitKey(1)

if __name__ == "__main__":
    # depth_cam = DepthCamera()
    obstacle_pub = rospy.Publisher("/obstacle_presence", Float32, queue_size=10)
    rospy.Subscriber("/camera/aligned_depth_to_color/image_raw", Image, depth_image_callback)

    rospy.spin()
