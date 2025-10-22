import cv2

def list_cameras():
    index = 0
    cameras = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            cameras.append(index)
        cap.release()
        index += 1
    return cameras

if __name__ == "__main__":
    detected_cameras = list_cameras()
    if detected_cameras:
        print("Detected cameras:", detected_cameras)
    else:
        print("No cameras detected.")