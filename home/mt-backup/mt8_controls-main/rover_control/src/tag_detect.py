#! /usr/bin/env python3
import pyrealsense2 as rs
import numpy as np
import cv2
import rospy
from std_msgs.msg import String

class Detection:
    def __init__(self):
        rospy.init_node("tag_detector")
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.pipeline.start(self.config)


        # Set up AR tag detection parameters
        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
        self.aruco_params = cv2.aruco.DetectorParameters_create()
        self.aruco_pub = rospy.Publisher("/aruco_tag_info", String, queue_size=10)

        # Camera intrinsics for distance calculation
        self.intrinsics = None
        while not self.intrinsics:
            frames = self.pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            self.intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics

    def __del__(self):
        self.pipeline.stop()

    def detect_ar_tag(self):
        # Wait for a coherent pair of frames: depth and color
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        if not color_frame or not depth_frame:
            return

        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())

        # Detect AR tags in the color image
        corners, ids, rejected = cv2.aruco.detectMarkers(color_image, self.aruco_dict, parameters=self.aruco_params)
        if ids is None:
            print("No AR Tag Detected. Keep Rotating right")
            self.aruco_pub.publish("0")
        # Draw a rectangle around each detected tag and calculate the distance to the center of the tag
        if ids is not None and len(ids) > 0:
            # Loop through all detected tags and draw a rectangle around them
            for i in range(len(ids)):
                corners[i] = corners[i].astype(int).reshape((-1, 1, 2))
                for corner in corners[i]:
                    cv2.circle(color_image, tuple(corner[0]), 5, (0, 255, 0), -1)
                center = corners[i].mean(axis=0).astype(int).squeeze()
                print(center)
                cv2.circle(color_image, tuple(center), 5, (0, 0, 255), -1)
                cv2.drawContours(color_image, [corners[i]], 0, (0, 255, 0), 2)

                # Calculate distance to the center of the tag
                depth = depth_frame.get_distance(center[0], center[1])
                distance = rs.rs2_deproject_pixel_to_point(self.intrinsics, [center[0], center[1]], depth)

                # Display distance and bounding box
                distance_str = f"Distance: {distance[2]:.2f} meters"
                cv2.putText(color_image, distance_str, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                bbox = cv2.boundingRect(corners[i])
                cv2.rectangle(color_image, (bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]+bbox[3]), (255, 0, 0), 2)
                print(f"Distance: {distance[2]:.2f} meters")
                msg_string = f"1 {distance[2]} {center[0]} {center[1]} {ids}"
                self.aruco_pub.publish(msg_string)

        # Display the color image
        cv2.imshow('AR Tag Detection', color_image)
        key = cv2.waitKey(1)
        if key == ord('q'):
            cv2.destroyAllWindows()
            exit()


if __name__ == '__main__':
    detection = Detection()
    while not rospy.is_shutdown():
        detection.detect_ar_tag()
