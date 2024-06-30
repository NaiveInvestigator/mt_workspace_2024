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
        align_to = rs.stream.color
        align = rs.align(align_to)

        frames = self.pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        aligned_depth_frame = rs.decimation_filter(2.0).process(aligned_frames.get_depth_frame())
        aligned_depth_frame = rs.spatial_filter().process(aligned_depth_frame)
        aligned_depth_frame = rs.temporal_filter().process(aligned_depth_frame)
        aligned_depth_frame = rs.hole_filling_filter().process(aligned_depth_frame)
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()

        # color_frame = frames.get_color_frame()
        # depth_frame = frames.get_depth_frame()

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        if not depth_frame or not color_frame:
            return False, None, None
        return True, depth_image, color_image

    def release(self):
        self.pipeline.stop()

    def release(self):
        self.pipeline.stop()
##

def calc_midpoint(x1, x2, y1, y2):
    return int((x1 + x2)/2), int((y1 + y2)/2)

rospy.init_node("aruco_detect")
tags = rospy.Publisher("/aruco_tag_info", String, queue_size=10)


detector_params = cv2.aruco.DetectorParameters()
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, detector_params)

#cap = cv2.VideoCapture(0)
depth_cam = DepthCamera()

if __name__ == "__main__":
    try:
        data_string = None
        while not rospy.is_shutdown():
            state, depth_frame, img = depth_cam.get_frame()
            
            corners, ids, rejected = aruco_detector.detectMarkers(img)
        
            if len(corners) > 0:
                aruco_state = "1"
                x, y = calc_midpoint(corners[0][0][0][0], corners[0][0][1][1], corners[0][0][2][0], corners[0][0][3][1])
                # try:
                #     distance = depth_frame[x, y]
                # except:
                #     pass
                if x > 479:
                    x = 479
                if y > 639:
                    y = 639

                distance = depth_frame[x, y]
                data_string = aruco_state + " " + str(distance) + " " + str(x) + " " + str(y) + " " + str(ids)
                print(f"Aruco tag ID: {ids}")
                print(f"Center: {x}, {y}")
                print(f"Distance: {distance}")

                topleft = corners[0][0][0]
                topright = corners[0][0][1]
                bottomright = corners[0][0][2]
                bottomleft = corners[0][0][3]

                x, y = calc_midpoint(topleft[0], bottomright[0], topleft[1], bottomright[1])

                cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
                cv2.rectangle(img, (int(topleft[0]), int(topleft[1])), (int(bottomright[0]), int(bottomright[1])), (255, 0, 0), 5)
            else:
                aruco_state = "0"
                data_string = aruco_state
            tags.publish(data_string)
            cv2.imshow("Aruco", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break   
        

#            if len(corners) > 0:
#                print(corners[0][0][0])
            
        
    finally:
        #cap.release()
        print("shutting dowb")
        depth_cam.release()