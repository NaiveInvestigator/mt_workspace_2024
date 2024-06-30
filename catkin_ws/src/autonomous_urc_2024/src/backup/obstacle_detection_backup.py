#! /usr/bin/env python3

import rospy
from std_msgs.msg import String, Float32
from sensor_msgs.msg import Imu, NavSatFix
from tf import transformations
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from math import radians, cos, sin, asin, sqrt, atan2, degrees
from time import sleep
from sbg_driver.msg import SbgGpsPos, SbgEkfEuler
import numpy as np
import pyrealsense2 as rs
import cv2

rospy.init_node("obstacle_detection")

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

        align_to = rs.stream.color
        align = rs.align(align_to)

        aligned_frames = align.process(frames)
        aligned_depth_frame = rs.decimation_filter(2.0).process(aligned_frames.get_depth_frame())
        aligned_depth_frame = rs.spatial_filter().process(aligned_depth_frame)
        aligned_depth_frame = rs.temporal_filter().process(aligned_depth_frame)
        aligned_depth_frame = rs.hole_filling_filter().process(aligned_depth_frame)
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        if not depth_frame or not color_frame:
            return False, None, None
        return True, depth_image, color_image

    def release(self):
        self.pipeline.stop()

if __name__ == "__main__":
    depth_cam = DepthCamera()
    obstacle_pub = rospy.Publisher("/obstacle_presence", Float32, queue_size=10)

    try:
        inflation_radius = 250
        obstacle_presence = 0.0
        while not rospy.is_shutdown():
            state, depth_frame, img = depth_cam.get_frame()
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

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break   

    finally:
        print("shutting dowb")
        depth_cam.release()

