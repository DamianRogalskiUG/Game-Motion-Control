import cv2
import mediapipe as mp
import numpy as np
from math import hypot
import pyautogui

# Drawing the lines on hand
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize the video capture from the default camera
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera feed
    data, image = cap.read()

    # Convert the image to RGB color space
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # Process the image to detect hands
    results = hands.process(image)

    # Convert the image back to BGR color space
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Check if hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks and connections on the image
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Get the coordinates of index finger tip and thumb tip
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            # Convert the normalized coordinates to pixel values
            x1, y1 = int(index_finger_tip.x * image.shape[1]), int(index_finger_tip.y * image.shape[0])
            x2, y2 = int(thumb_tip.x * image.shape[1]), int(thumb_tip.y * image.shape[0])

            # Draw circles at the finger tips
            cv2.circle(image, (x1, y1), 13, (255, 0, 0), cv2.FILLED)
            cv2.circle(image, (x2, y2), 13, (255, 0, 0), cv2.FILLED)

            # Draw a line between the finger tips
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 3)

            # Calculate the length between finger tips using Euclidean distance
            length = hypot(x2 - x1, y2 - y1)

            # Interpolate the length to get volume control values
            vol = np.interp(length, [30, 350], [0, 1])
            volbar = np.interp(length, [30, 350], [400, 150])
            volper = np.interp(length, [30, 350], [0, 100])

            # Move the mouse pointer to the index finger tip
            pyautogui.moveTo(x1, y1)

            # Press "r" key if length is less than 90
            if int(length) < 90:
                pyautogui.press("r")

            # Draw volume bar and percentage text on the image
            cv2.rectangle(image, (50, 150), (85, 400), (0, 0, 255), 4)
            cv2.rectangle(image, (50, int(volbar)), (85, 400), (0, 0, 255), cv2.FILLED)
            cv2.putText(image, f"{int(volper)}%", (10, 40), cv2.FONT_ITALIC, 1, (0, 255, 98), 3)

    # Display the image with hand tracking information
    cv2.imshow('Handtracker', image)

    # Wait for a key press event
    cv2.waitKey(1)
