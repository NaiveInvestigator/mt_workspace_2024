#! /usr/bin/env python3
import rospy
from std_msgs.msg import String, Float32
import numpy as np
import time
import cv2
import pyrealsense2 as rs
from ultralytics import YOLO
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

def depth_image_callback(data):
    global depth_frame
    bridge = CvBridge()
    try:
        # Assuming the depth image is encoded in 16UC1 format
        depth_frame = bridge.imgmsg_to_cv2(data, desired_encoding="16UC1")
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
    
    results = model.predict(img)
    result = results[0]

    id_name_mapping = {value:key for key, value in result.names.items()}

    object_x_centre, object_y_centre = None, None
    object_top_left = None
    object_bottom_right = None

    data_string = "0"
    object_max_conf = float("-inf")

    # for obj in result.boxes.data:
    #     obj = obj.tolist()
    #     if obj[4] > conf_threshold: #and obj[5] == float(id_name_mapping[trg_label]):
    #         object_x_centre = int((obj[0] + obj[2]) / 2)
    #         object_y_centre = int((obj[1] + obj[3]) / 2)
    #         top_left = (int(obj[0]), int(obj[1]))
    #         bottom_right = (int(obj[2]), int(obj[3]))
    #         # break
    #         cv2.circle(img, (object_x_centre, object_y_centre), 5, (255, 0, 0), -1)
    #         cv2.rectangle(img, (top_left[0], top_left[1]), (bottom_right[0], bottom_right[1]), (0, 0, 255), 3)
    #         cv2.putText(img, "Object", top_left, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
    #         object_state = "1"
    #         x, y = object_x_centre, object_y_centre
    #         distance = depth_frame[y, x]
    #         data_string = object_state + " " + str(distance) + " " + str(x) + " " + str(y) 
    #         print(f"Center: {x}, {y}")
    #         print(f"Distance: {distance}")

    #         break
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

    object.objects.publish(data_string)      

class Object:
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

    rospy.Subscriber("/camera/color/image_raw", Image, rgb_image_callback)
    rospy.Subscriber("/camera/aligned_depth_to_color/image_raw", Image, depth_image_callback)
    rospy.spin()

    # aruco_reached_pub = rospy.Publisher("/aruco_reached", Float32, queue_size=10)
