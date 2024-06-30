#! /usr/bin/env python3
import rospy
from std_msgs.msg import String, Float32
import numpy as np
import time
import cv2
import pyrealsense2 as rs
import cv2
from ultralytics import YOLO

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

        # depth_frame = frames.get_depth_frame()
        # color_frame = frames.get_color_frame()

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        if not depth_frame or not color_frame:
            return False, None, None
        return True, depth_image, color_image

    def release(self):
        self.pipeline.stop()


class Object:

    def calc_midpoint(self, x1, x2, y1, y2):
        return int((x1 + x2)/2), int((y1 + y2)/2)

    objects = rospy.Publisher("/object_info", String, queue_size=10)

if __name__ == "__main__":
    rospy.init_node("object_detect")

    object = Object()

    OBJECT = "Mallet"
    if OBJECT == "Mallet":
        model = YOLO("weights/mallet_coloured_small.pt")
    else:
        model = YOLO("weights/bottle_grayscale_small.pt")
    conf_threshold = 0.7

    
    depth_cam = DepthCamera()

    # aruco_reached_pub = rospy.Publisher("/aruco_reached", Float32, queue_size=10)

    try:
        data_string = None
        while not rospy.is_shutdown():
            state, depth_frame, img = depth_cam.get_frame()
            results = model.predict(img)
            result = results[0]

            id_name_mapping = {value:key for key, value in result.names.items()}

            object_x_centre, object_y_centre = None, None
            object_top_left = None
            object_bottom_right = None

            data_string = "0"
            object_max_conf = float("-inf")
        
            for obj in result.boxes.data:
                obj = obj.tolist()
                if obj[4] >= conf_threshold: #and obj[5] == float(id_name_mapping[trg_label]):
                    if obj[4] > object_max_conf:
                        object_x_centre = int((obj[0] + obj[2]) / 2)
                        object_y_centre = int((obj[1] + obj[3]) / 2)
                        object_top_left = (int(obj[0]), int(obj[1]))
                        object_bottom_right = (int(obj[2]), int(obj[3]))
                        object_max_conf = obj[4]

            object_state = "1"
            x, y = object_x_centre, object_y_centre
            distance = depth_frame[y, x]
            data_string = object_state + " " + str(distance) + " " + str(x) + " " + str(y) 
            print(f"Center: {x}, {y}")
            print(f"Distance: {distance}")

            cv2.circle(img, (object_x_centre, object_y_centre), 5, (255, 0, 0), -1)
            cv2.rectangle(img, (object_top_left[0], object_top_left[1]), (object_bottom_right[0], object_bottom_right[1]), (0, 0, 255), 3)
            cv2.putText(img, "Object", object_top_left, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            object.objects.publish(data_string)  
            cv2.imshow("RGB Frame", img)    

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break   
        
    finally:
        print("shutting dowb")
        depth_cam.release()