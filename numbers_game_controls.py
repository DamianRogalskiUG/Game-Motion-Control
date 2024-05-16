import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
from tensorflow.keras.models import load_model
from PIL import Image, ImageOps
import time
import numpy as np
import math
import pyautogui

# Load the model
model = load_model("Model/hand_gesture_model.keras", compile=False)

# Load the labels
class_names = open("Model/labels.txt", "r").readlines()

# Load the model
model = load_model("Model/hand_gesture_model.keras", compile=False)

# Load the labels
class_names = open("Model/labels.txt", "r").readlines()


# declaring Camera Capture
cap = cv2.VideoCapture(0)

# declaring the hand detector
detector = HandDetector(maxHands=1)

# declaring an offset (margin) and an image size for images
offset = 40
image_size = 300

# destination where images are saved
image_destination_folder = "Data/0"

# counter to count captured images
counter = 0


# function to press correct buttons after detecting the gesture (for numbers game)
def control_game(prediction):
    if np.array_equal(prediction, [[1, 0, 0, 0]]):
        pyautogui.press("1")
    elif np.array_equal(prediction, [[0, 1, 0, 0]]):
        pyautogui.press("2")
    elif np.array_equal(prediction, [[0, 0, 1, 0]]):
        pyautogui.press("3")
    elif np.array_equal(prediction, [[0, 0, 0, 1]]):
        pyautogui.press("4")


while True:
    # reading a data from camera
    data, image = cap.read()

    # detecting hands
    hands, image = detector.findHands(image)
    if hands:
        hand = hands[0]

        # setting the bounding box
        x, y, width, height = hand['bbox']

        # declaring an empty array of ones
        image_white = np.ones((image_size, image_size, 3), np.uint8) * 255

        # crop the image
        image_crop = image[y - offset:y + height + offset, x - offset:x + width + offset]

        # shape of the cropped image
        image_crop_shape = image_crop.shape

        # aspect ratio to determine if height is bigger than width or not
        aspect_ratio = height / width

        # if height is bigger

        # code calculates how much to resize the image and makes adjustments to the image white size
        # after that it predicts the current image
        if aspect_ratio > 1:

            k = image_size / height
            calculated_width = math.ceil(k * width)
            image_resize = cv2.resize(image_crop, (calculated_width, image_size))
            image_resize_shape = image_resize.shape
            width_gap = math.ceil((image_size-calculated_width) / 2)
            image_white[:, width_gap:calculated_width + width_gap] = image_resize
            image_white_predict = np.expand_dims(image_white, axis=0)
            prediction = model.predict(image_white_predict)
            print(prediction)
            control_game(prediction)

        # if width is bigger
        else:
            # try except to prevent crashes with to big image sizesss
            try:
                k = image_size / width
                calculated_height = math.ceil(k * height)
                image_resize = cv2.resize(image_crop, (calculated_height, image_size))
                image_resize_shape = image_resize.shape
                height_gap = math.ceil((image_size-calculated_height) / 2)
                image_white[height_gap:calculated_height + height_gap, :] = image_resize
                image_white_predict = np.expand_dims(image_white, axis=0)
                prediction = model.predict(image_white_predict)
                control_game(prediction)
                print(prediction)
            except:
                print("can't fit an image")
        # showing camera feeds for cropped image and a white image
        cv2.imshow("ImageCrop", image_crop)
        cv2.imshow("ImageWhite", image_white)
312221241111433323123222313111
    # showing main camera feed
    cv2.imshow("Image", image)
    # cv2.waitKey(1)

    # this part is for saving images if needed
    key = cv2.waitKey(1)
    if key == ord("s"):
        counter += 1
        cv2.imwrite(f"{image_destination_folder}/Image_{time.time()}.jpg", image_white)
        print(counter)
