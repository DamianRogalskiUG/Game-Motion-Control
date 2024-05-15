import cv2
import mediapipe as mp
import pyautogui

# Drawing the lines on hand
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# capturing camera feed
cap = cv2.VideoCapture(0)

# setting key states (so the hand position will keep the key down till it changes position)
key_states = {'width': False, 'a': False, 's': False, 'd': False}

# gesture variable is to present current gesture on screen
gesture = None

while True:
    # Reading frame from camera
    data, image = cap.read()

    # Flip the image horizontally for a later selfie-view display
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # Process the image frame to detect hands
    results = hands.process(image)

    # Convert the image back to BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # If hands are detected in the frame
    if results.multi_hand_landmarks:
        # For each detected hand
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw the landmarks and connections on the image
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Get the x and y coordinates of the middle finger's MCP (Metacarpophalangeal) joint
            center_x = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
            center_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y

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
                pyautogui.keyDown("width")
                key_states['width'] = True
                gesture = "width"
            else:
                if key_states['s']:
                    pyautogui.keyUp("s")
                    key_states['s'] = False
                    gesture = None
                if key_states['width']:
                    pyautogui.keyUp("width")
                    key_states['width'] = False
                    gesture = None

            # Display the current gesture on the image
            cv2.putText(image, f'Gesture: {gesture}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                        cv2.LINE_AA)

    # Show the image with detected hands and gestures
    cv2.imshow('Handtracker', image)
    cv2.waitKey(1)
