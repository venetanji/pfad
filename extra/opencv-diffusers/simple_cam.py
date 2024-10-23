import cv2
import numpy as np

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# set camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = cap.read()
    cv2.imshow("frame", frame)
    flip = cv2.flip(frame, 1)
    cv2.imshow("flip", flip)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break