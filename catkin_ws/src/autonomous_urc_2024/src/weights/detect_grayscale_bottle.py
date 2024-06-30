import cv2 
from ultralytics import YOLO

# model = YOLO('yolov8n-25-2-24-40e.pt')  
model = YOLO("bottle_grayscale_small.pt")  
cap = cv2.VideoCapture(0)

conf_threshold = 0.7

while True:
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    results = model.predict(frame)
    result = results[0]
    #im_array = result.plot()
    id_name_mapping = {value:key for key, value in result.names.items()}

    bottle_x_centre, bottle_y_centre = None, None
    top_left = None
    bottom_right = None

    for obj in result.boxes.data:
        obj = obj.tolist()
        if obj[4] > conf_threshold: #and obj[5] == float(id_name_mapping[trg_label]):
            bottle_x_centre = int((obj[0] + obj[2]) / 2)
            bottle_y_centre = int((obj[1] + obj[3]) / 2)
            top_left = (int(obj[0]), int(obj[1]))
            bottom_right = (int(obj[2]), int(obj[3]))
            # break
            cv2.circle(frame, (bottle_x_centre, bottle_y_centre), 5, (255, 0, 0), -1)
            cv2.rectangle(frame, (top_left[0], top_left[1]), (bottom_right[0], bottom_right[1]), (0, 0, 255), 3)
            cv2.putText(frame, "Bottle", top_left, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.waitKey(0)
cv2.destroyAllWindows()
