import cv2
import mediapipe as mp
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
            center_x = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
            center_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
            if center_x > 0.7:
                print("right")
            elif center_x < 0.3:
                print("left")

            if center_y > 0.7:
                print("down")
            elif center_y < 0.3:
                print("up")
    cv2.imshow('Handtracker', image)
    cv2.waitKey(1)
