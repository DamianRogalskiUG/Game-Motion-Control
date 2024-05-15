import cv2
import mediapipe as mp
import pyautogui
import math

from tensorflow.keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np


# Drawing the lines on hand
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)

model = load_model("Model/hand_gesture_model.keras", compile=False)

class_names = open("Model/labels.txt", "r").readlines()


key_states = {'w': False, 'a': False, 's': False, 'd': False}
gesture = None

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

            cv2.putText(image, f'Gesture: {gesture}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                        cv2.LINE_AA)


    cv2.imshow('Handtracker', image)
    cv2.waitKey(1)