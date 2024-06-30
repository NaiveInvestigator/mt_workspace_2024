#! /usr/bin/env python3

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from rover_control.msg import ArucoInfo
import numpy as np
import cv2

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
tags = rospy.Publisher("/aruco_tag_info", ArucoInfo, queue_size=10)

aruco_type = "DICT_4X4_50"

arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[aruco_type])

arucoParams = cv2.aruco.DetectorParameters_create()

img = []
depth_frame = []

h, w = 1, 1

def handle_color_frame(msg: Image):
    # print("got color frame")
    global x, y, img
    img = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, -1)

def handle_depth_frame(msg: Image):
    global distance, depth_frame
    depth_frame = np.frombuffer(msg.data, dtype=np.uint16).reshape(msg.height, msg.width)

color_frame_sub = rospy.Subscriber("/camera/color/image_raw", Image, handle_color_frame)
depth_frame_sub = rospy.Subscriber("/camera/aligned_depth_to_color/image_raw", Image, handle_depth_frame)

if __name__ == "__main__":
    #x, y = 3, 5
    #distance = 4
    # try:
    aruco_msg = ArucoInfo()
    aruco_msg.detected = False
    aruco_msg.distance = -1
    aruco_msg.x = -1
    aruco_msg.y = -1
    aruco_msg.id = -1
    while not rospy.is_shutdown(): #cap.isOpened() and not rospy.is_shutdown():
        if len(img) == 0:
            continue

        corners, ids, rejected = cv2.aruco.detectMarkers(img, arucoDict, parameters=arucoParams)

        if len(corners) > 0:
            aruco_msg.detected = True
            
            x, y = calc_midpoint(corners[0][0][0][0], corners[0][0][2][0], corners[0][0][0][1], corners[0][0][2][1])
            
            # print(x, y)
            try:
                distance = depth_frame[x][y]
            except IndexError:
                distance = -1
            
            print(ids)
            aruco_msg.distance = distance
            aruco_msg.x = x
            aruco_msg.y = y
            aruco_msg.id = ids[0][0]

            cv2.circle(img, (x, y), 4, (0, 0, 255))
            cv2.rectangle(img, (corners[0][0][0][0], corners[0][0][0][1]), (corners[0][0][2][0], corners[0][0][2][1]), (0, 255, 0), 2)
            
            tags.publish(aruco_msg)
            rospy.loginfo(f"{aruco_msg.id} Tag detected at {aruco_msg.x}, {aruco_msg.y} with distance {aruco_msg.distance}\t{distance}")

            #print(depth_frame)

        # img_depth_joined = np.concatenate((img, depth_frame), axis=1)

        cv2.imshow("Aruco Detection", img)
        # cv2.imshow("Depth", depth_frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
    # except Exception as e:
    #     print(e)

        
        #cap.release()
    cv2.destroyAllWindows()
    pass
