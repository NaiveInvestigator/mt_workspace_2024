#!/usr/bin/env python3

import rospy 
from sensor_msgs.msg import Image, PointCloud2
import sensor_msgs.point_cloud2 as pc2
import cv2
import numpy as np
from cv_bridge import CvBridge

def scan_read(msg):
    try:
        # Convert ROS Image message to OpenCV image
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

        # Process or use the OpenCV image as needed
        cv2.imshow("Received Image", cv_image)
        cv2.waitKey(1)

    except Exception as e:
        rospy.logerr("Error processing image: %s", str(e))
    

def scan_listen():
    rospy.init_node('realsense_scan_reader', anonymous=True)
    rospy.Subscriber("/realsense/color/image_raw", Image, scan_read)
    rospy.spin()


if __name__ == '__main__':
    scan_listen()
