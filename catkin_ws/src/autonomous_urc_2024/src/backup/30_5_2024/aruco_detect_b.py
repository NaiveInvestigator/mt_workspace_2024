#! /usr/bin/env python3
import rospy
from std_msgs.msg import String, Float32
import numpy as np
import time
import cv2
import pyrealsense2 as rs
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

def depth_image_callback(data):
    global depth_frame
    bridge = CvBridge()
    try:
        # Assuming the depth image is encoded in 16UC1 format
        depth_frame = bridge.imgmsg_to_cv2(data, desired_encoding="16UC1")

        # cv2.imshow("Depth frame", depth_frame)    
        # cv2.waitKey(1) 

    except CvBridgeError as e:
        rospy.logerr("CvBridge Error: {0}".format(e))
        return

def rgb_image_callback(data):
    data_string = None

    bridge = CvBridge()
    try:
        # Assuming the depth image is encoded in 16UC1 format
        img = bridge.imgmsg_to_cv2(data, desired_encoding="bgr8")
    except CvBridgeError as e:
        rospy.logerr("CvBridge Error: {0}".format(e))
        return
    
    corners, ids, rejected = cv2.aruco.detectMarkers(img, aruco.arucoDict, parameters=aruco.arucoParams)

    if len(corners) > 0:
        aruco_state = "1"
        topleft = corners[0][0][0]
        topright = corners[0][0][1]
        bottomright = corners[0][0][2]
        bottomleft = corners[0][0][3]
        x, y = aruco.calc_midpoint(topleft[0], bottomright[0], topleft[1], bottomright[1])
        distance = depth_frame[y, x]
        data_string = aruco_state + " " + str(distance) + " " + str(x) + " " + str(y) + " " + str(ids)

        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        cv2.rectangle(img, (int(topleft[0]), int(topleft[1])), (int(bottomright[0]), int(bottomright[1])), (255, 0, 0), 5)

        print(f"Aruco tag ID: {ids}")
        print(f"Center: {x}, {y}")
        print(f"Distance: {distance}")
    else:
        aruco_state = "0"
        data_string = aruco_state
        # aruco_reached_pub.publish(0.0)
    aruco.tags.publish(data_string)  

    cv2.imshow("RGB Frame", img)    
    cv2.waitKey(1) 

class Aruco:

    def calc_midpoint(self, x1, x2, y1, y2):
        return int((x1 + x2)/2), int((y1 + y2)/2)

    ARUCO_DICT = {
        "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
        "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
        "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
        "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
        "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
        "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
        "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
        "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
        "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
        "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
        "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
        "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
        "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
        "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
        "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
        "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
        "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
        "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
        "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
        "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
        "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
    }

    tags = rospy.Publisher("/aruco_tag_info", String, queue_size=10)

    aruco_type = "DICT_4X4_50"

    arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[aruco_type])

    arucoParams = cv2.aruco.DetectorParameters()

if __name__ == "__main__":
    rospy.init_node("aruco_detect")

    depth_frame = None

    aruco = Aruco()
    rospy.Subscriber("/camera/color/image_raw", Image, rgb_image_callback)
    rospy.Subscriber("/camera/aligned_depth_to_color/image_raw", Image, depth_image_callback)
    rospy.spin()

    # aruco_reached_pub = rospy.Publisher("/aruco_reached", Float32, queue_size=10)
