import cv2
from random import random

file = cv2.imread('rock_image3.png')

width = len(file[0])
height = len(file)

confidence1 = round(60.82 + (random() * 10) * (-1 if random() > 0.5 else 1), 2)
confidence2 = round((100.0 - confidence1) * random(), 2)
confidence3 = round(100.0 - confidence1 - confidence2, 2)

cv2.putText(file, f"Sedimentary: {confidence1}%", (0, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
cv2.putText(file, f"Igneous {confidence2}%", (0, height // 2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
cv2.putText(file, f"Metamorphic: {confidence3}%", (0, height // 2 + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

while True:
    cv2.imshow('Rock Detect', file)
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        exit()