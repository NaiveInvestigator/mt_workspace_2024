import cv2
import numpy as np
print(cv2.__version__)
cap = cv2.VideoCapture(2)

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters()

def center_cal(corner):
    cen_x = (corner[0][0]+corner[1][0])/2
    cen_y = (corner[0][1]+corner[2][1])/2

    return (cen_x, cen_y)

def calculateangle(marker1, marker2, marker3):
    cen_marker0 = list(center_cal(marker1))
    cen_marker1 = list(center_cal(marker2))
    cen_marker2 = list(center_cal(marker3))

    v1= cen_marker1 - cen_marker0
    v2 = cen_marker2 - cen_marker0 

    dot_p= np.dot(v1, v2)
    mag_1 = np.linalg.norm(v1)
    mag_2 = np.linalg.norm(v2)

    cos_theta = dot_p / (mag_1 * mag_2)
    angle_radians = np.arccos(cos_theta)
    
    angle_degrees = np.degrees(angle_radians)

    return angle_degrees





while True:
    ret, frame = cap.read()

   

    # Detect ArUco markers in the frame
    corners, ids, reject = cv2.aruco.detectMarkers(frame, aruco_dict, parameters=parameters)

    while ids!=None and len(ids) <= 2:
        ret, frame = cap.read()

        corners, ids, reject = cv2.aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)


        print(ids)

    # Draw the detected markers on the frame
    cv2.aruco.drawDetectedMarkers(frame, corners, ids)
    if ids!=None and len(ids)==3:
    # Calculate angle when two markers are detected
        angle = calculateangle(corners[np.where(ids == ids[0])], corners[np.where(ids == ids[1])], corners[np.where(ids == ids[2])])
        print(f"Calculated Angle: {angle} degrees")

    # Display the frame
    cv2.imshow("ArUco Marker Detection", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF== ord('q'):
      break

cap.release()
cv2.destroyAllWindows()