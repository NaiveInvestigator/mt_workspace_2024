import cv2
import numpy as np

def calculate_angle(p1, p2, p3):
    v1 = p1 - p2
    v2 = p3 - p2

    dot_p= np.dot(v1, v2)
    mag_1 = np.linalg.norm(v1)
    mag_2 = np.linalg.norm(v2)

    cos_theta = dot_p / (mag_1 * mag_2)
    angle_radians = np.arccos(cos_theta)
    
    angle_degrees = np.degrees(angle_radians)

    return angle_degrees

def mouse_call(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))

    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    if len(points) == 3:
        angle = calculate_angle(np.array(points[0]), np.array(points[1]), np.array(points[2]))
        
        print(f"Angle: {angle}")



cap = cv2.VideoCapture(0)
points = []

cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame', mouse_call)

while True:
    ret, frame = cap.read()

    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()