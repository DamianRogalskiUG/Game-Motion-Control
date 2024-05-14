import cv2
import mediapipe as mp
import numpy as np
from math import hypot
import pyautogui



# Drawing the lines on hand
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()


cap = cv2.VideoCapture(0)


while True:
    data, image = cap.read()
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            x1, y1 = int(index_finger_tip.x * image.shape[1]), int(index_finger_tip.y * image.shape[0])
            x2, y2 = int(thumb_tip.x * image.shape[1]), int(thumb_tip.y * image.shape[0])
            cv2.circle(image, (x1, y1), 13, (255, 0, 0), cv2.FILLED)
            cv2.circle(image, (x2, y2), 13, (255, 0, 0), cv2.FILLED)
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 3)
            length = hypot(x2 - x1, y2 - y1)
            vol = np.interp(length, [30, 350], [0, 1])
            volbar = np.interp(length, [30, 350], [400, 150])
            volper = np.interp(length, [30, 350], [0, 100])

            print(vol, int(length))

            pyautogui.moveTo(x1, y1)

            if int(length) < 90:
                pyautogui.press("r")

            cv2.rectangle(image, (50, 150), (85, 400), (0, 0, 255), 4)
            cv2.rectangle(image, (50, int(volbar)), (85, 400), (0, 0, 255), cv2.FILLED)
            cv2.putText(image, f"{int(volper)}%", (10, 40), cv2.FONT_ITALIC, 1, (0, 255, 98), 3)





    cv2.imshow('Handtracker', image)
    cv2.waitKey(1)