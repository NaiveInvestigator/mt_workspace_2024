#! /usr/bin/env python3
import rospy
from std_msgs.msg import String
import numpy as np
import time
import cv2
import pyrealsense2 as rs

## This portion is for the realsense
class DepthCamera:
    def __init__(self):
        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)



        # Start streaming
        self.pipeline.start(config)

    def get_frame(self):
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        if not depth_frame or not color_frame:
            return False, None, None
        return True, depth_image, color_image

    def release(self):
        self.pipeline.stop()
##

def calc_midpoint(x1, x2, y1, y2):
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

rospy.init_node("aruco_detect")
tags = rospy.Publisher("/aruco_tag_info". String, queue_size=10)

aruco_type = "DICT_4X4_50"

arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[aruco_type])

arucoParams = cv2.aruco.DetectorParameters_create()

#cap = cv2.VideoCapture(0)
depth_cam = DepthCamera()

if __name__ == "__main__":
    try:
        data_string = None
        while not rospy.is_shutdown():
            state, depth_frame, img = depth_cam.get_frame()
            corners, ids, rejected = cv2.aruco.detectMarkers(img, arucoDict, parameters=arucoParams)
        
            if len(corners) > 0:
                aruco_state = "1"
                x, y = calc_midpoint(corners[0][0][0][0], corners[0][0][1][1], corners[0][0][2][0], corners[0][0][3][1])
                distance = depth_frame[x, y]
                data_string = aruco_state + " " + str(distance) + " " + str(x) + " " + str(y) + " " + str(ids)
                print(f"Aruco tag ID: {ids}")
                print(f"Center: {x}, {y}")
                print(f"Distance: {distance}")
            else:
                aruco_state = "0"
                data_string = aruco_state
            tags.publish(data_string)
        

#            if len(corners) > 0:
#                print(corners[0][0][0])
            
        
    finally:
        #cap.release()
        print("shutting dowb")
        depth_cam.release()
