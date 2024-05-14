import cv2
import mediapipe as mp
import pyautogui
import numpy as np
from math import hypot

# Initialize MediaPipe hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Initialize the camera
cap = cv2.VideoCapture(0)

# Initialize key states and gesture
key_states = {'w': False, 'a': False, 's': False, 'd': False}
gesture = None

# Volume control variables
volbar = 400
volper = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip horizontally
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process hand landmarks
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            center_x = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
            center_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_finger_base = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]

            # Check hand position for controlling keys
            if center_x > 0.7:
                pyautogui.keyDown("d")
                key_states['d'] = True
                gesture = "d"
            elif center_x < 0.3:
                pyautogui.keyDown("a")
                key_states['a'] = True
                gesture = "a"
            else:
                if key_states['d']:
                    pyautogui.keyUp("d")
                    key_states['d'] = False
                    gesture = None
                if key_states['a']:
                    pyautogui.keyUp("a")
                    key_states['a'] = False
                    gesture = None

            if center_y > 0.7:
                pyautogui.keyDown("s")
                key_states['s'] = True
                gesture = "s"
            elif center_y < 0.3:
                pyautogui.keyDown("w")
                key_states['w'] = True
                gesture = "w"
            else:
                if key_states['s']:
                    pyautogui.keyUp("s")
                    key_states['s'] = False
                    gesture = None
                if key_states['w']:
                    pyautogui.keyUp("w")
                    key_states['w'] = False
                    gesture = None

            # Volume control based on thumb and index finger distance
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            x1, y1 = int(index_finger_tip.x * img.shape[1]), int(index_finger_tip.y * img.shape[0])
            x2, y2 = int(thumb_tip.x * img.shape[1]), int(thumb_tip.y * img.shape[0])
            cv2.circle(img, (x1, y1), 13, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 13, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
            length = hypot(x2 - x1, y2 - y1)
            vol = np.interp(length, [30, 350], [0, 1])
            volbar = np.interp(length, [30, 350], [400, 150])
            volper = np.interp(length, [30, 350], [0, 100])

            print(vol, int(length))


            if int(length) < 90:
                pyautogui.press("volumeup")

            cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 255), 4)
            cv2.rectangle(img, (50, int(volbar)), (85, 400), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, f"{int(volper)}%", (10, 40), cv2.FONT_ITALIC, 1, (0, 255, 98), 3)

    cv2.imshow('Handtracker', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
