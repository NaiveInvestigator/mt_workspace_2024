import cv2 
import numpy as np
import pyrealsense2 as rl_cam

pipeline = rl_cam.pipeline()
config = rl_cam.config()
config.enable_stream(rl_cam.stream.color, 640, 480, rl_cam.format.bgr8, 30)
pipeline.start(config)

detector_params = cv2.aruco.DetectorParameters()
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, detector_params)

#cap = cv2.VideoCapture(1)

while True:
    #ret, frame = cap.read()
    frame = pipeline.wait_for_frames()
    frame = frame.get_color_frame()
    frame = np.asanyarray(frame.get_data())


    corners, ids, rejected = aruco_detector.detectMarkers(frame)

    if ids is not None:
        corners = corners[0][0]
        cv2.rectangle(frame, (int(corners[0][0]), int(corners[0][1])), (int(corners[2][0]), int(corners[2][1])), (0, 255, 0), 2)
        center = ( int( (corners[0][0] + corners[2][0]) // 2), int( (corners[0][1] + corners[2][1]) // 2) )
        cv2.circle(frame, center, 5, (0, 0, 255), -1)



    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.waitKey(0)
cv2.destroyAllWindows()






