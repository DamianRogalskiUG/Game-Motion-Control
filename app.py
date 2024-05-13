import cv2
import mediapipe as mp
import pyautogui
import math

# Drawing the lines on hand
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)

key_states = {'w': False, 'a': False, 's': False, 'd': False}

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
            elif center_x < 0.3:
                pyautogui.keyDown("a")
                key_states['a'] = True
            else:
                if key_states['d']:
                    pyautogui.keyUp("d")
                    key_states['d'] = False
                if key_states['a']:
                    pyautogui.keyUp("a")
                    key_states['a'] = False

            if center_y > 0.7:
                pyautogui.keyDown("s")
                key_states['s'] = True
            elif center_y < 0.3:
                pyautogui.keyDown("w")
                key_states['w'] = True
            else:
                if key_states['s']:
                    pyautogui.keyUp("s")
                    key_states['s'] = False
                if key_states['w']:
                    pyautogui.keyUp("w")
                    key_states['w'] = False

            # if prev_hand_position and prev_hand_position != (center_x, center_y):
            #     for key in pyautogui.KEYBOARD_KEYS:
            #         pyautogui.keyUp(key)

            angle = math.degrees(math.atan2(index_finger_tip.y - index_finger_base.y, index_finger_tip.x - index_finger_base.x))

            # if angle <= -45 and angle > -135:
            #     pyautogui.click()
            # prev_hand_position = (center_x, center_y)

    cv2.imshow('Handtracker', image)
    cv2.waitKey(1)
