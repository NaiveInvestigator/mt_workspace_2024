#! /usr/bin/env python3
import rospy
from std_msgs.msg import String
import numpy as np
import time
import cv2
import pyrealsense2 as rs
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

rospy.init_node("mallet_detect")
mallets = rospy.Publisher("/mallet_info", String, queue_size=10)

#cap = cv2.VideoCapture(0)
depth_cam = DepthCamera()

if __name__ == "__main__":
    model = YOLO("/home/mtbase/catkin_ws/src/autonomous_urc_2024/src/weights/mallet_coloured_small.pt")
    conf_threshold = 0.7
    try:
        data_string = None
        while not rospy.is_shutdown():
            state, depth_frame, img = depth_cam.get_frame()
            
            results = model.predict(img)
            result = results[0]

            id_name_mapping = {value:key for key, value in result.names.items()}

            mallet_x_centre, mallet_y_centre = None, None
            mallet_top_left = None
            mallet_bottom_right = None

            data_string = "0"
            mallet_max_conf = float("-inf")
        
            for obj in result.boxes.data:
                obj = obj.tolist()
                if obj[4] >= conf_threshold: #and obj[5] == float(id_name_mapping[trg_label]):
                    if obj[4] > mallet_max_conf:
                        mallet_x_centre = int((obj[0] + obj[2]) / 2)
                        mallet_y_centre = int((obj[1] + obj[3]) / 2)
                        mallet_top_left = (int(obj[0]), int(obj[1]))
                        mallet_bottom_right = (int(obj[2]), int(obj[3]))
                        mallet_max_conf = obj[4]

            if mallet_x_centre is not None:

                mallet_state = "1"
                x, y = mallet_x_centre, mallet_y_centre
                # try:
                #     distance = depth_frame[x, y]
                # except:
                #     pass
                if x > 479:
                    x = 479
                if y > 639:
                    y = 639

                distance = depth_frame[x, y]

                data_string = mallet_state + " " + str(distance) + " " + str(x) + " " + str(y) 
                print(f"Center: {x}, {y}")
                print(f"Distance: {distance}")

                cv2.circle(img, (mallet_x_centre, mallet_y_centre), 5, (255, 0, 0), -1)
                cv2.rectangle(img, (mallet_top_left[0], mallet_top_left[1]), (mallet_bottom_right[0], mallet_bottom_right[1]), (0, 0, 255), 3)
                cv2.putText(img, "mallet", mallet_top_left, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            mallets.publish(data_string)  
            cv2.imshow("RGB Frame", img)    

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break              
        
    finally:
        #cap.release()
        print("shutting dowb")
        depth_cam.release()