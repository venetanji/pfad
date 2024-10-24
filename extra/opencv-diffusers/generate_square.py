import cv2
import numpy as np

# Define the size of the window and the square
window_size = 500
square_size = 100

# Create a black image
image = np.zeros((window_size, window_size, 3), dtype=np.uint8)

# Define the center and the angle of rotation
center = (window_size // 2, window_size // 2)
angle = 0

while True:
    # Create a copy of the black image
    img_copy = image.copy()

    # Calculate the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    # Define the points of the square
    points = np.array([
        [center[0] - square_size // 2, center[1] - square_size // 2],
        [center[0] + square_size // 2, center[1] - square_size // 2],
        [center[0] + square_size // 2, center[1] + square_size // 2],
        [center[0] - square_size // 2, center[1] + square_size // 2]
    ])

    # Rotate the points
    rotated_points = cv2.transform(np.array([points]), rotation_matrix)[0]

    # Draw the square
    cv2.polylines(img_copy, [np.int32(rotated_points)], isClosed=True, color=(255, 255, 255), thickness=2)

    # Show the image
    cv2.imshow('Rotating Square', img_copy)

    # Increment the angle
    angle += 1

    # Break the loop if 'q' is pressed
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release the window
cv2.destroyAllWindows()