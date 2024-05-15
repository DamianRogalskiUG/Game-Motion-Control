import time
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier

import pyautogui


from tensorflow.keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL

import numpy as np
import math

# Load the model
model = load_model("Model/hand_gesture_model.keras", compile=False)

# Load the labels
class_names = open("Model/labels.txt", "r").readlines()

# Load the model
model = load_model("Model/hand_gesture_model.keras", compile=False)

# Load the labels
class_names = open("Model/labels.txt", "r").readlines()

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1
data = np.ndarray(shape=(1, 300, 300, 3), dtype=np.uint8)

# Replace this with the path to your image
image = Image.open("Data/Test/II/Image_1715723937.1327062.jpg").convert("RGB")

size = (300, 300)
image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

# turn the image into a numpy array
image_array = np.asarray(image)

# Normalize the image
normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

# Load the image into the array
data[0] = normalized_image_array

# # Predicts the model
# prediction = model.predict(data)
# index = np.argmax(prediction)
# class_name = class_names[index]
# confidence_score = prediction[0][index]

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
# classifier = Classifier("Model/hand_gesture_model.keras", "Model/labels.txt")

offset = 40
image_size = 300

folder = "Data/IV"
counter = 0

labels = ["I", "II", "III", "IV"]

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
    success, image = cap.read()
    hands, image = detector.findHands(image)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        image_white = np.ones((image_size, image_size, 3), np.uint8) * 255

        # crop the image
        image_crop = image[y - offset:y + h + offset, x - offset:x + w + offset]

        image_crop_shape = image_crop.shape

        aspect_ratio = h / w

        if aspect_ratio > 1:
            k = image_size / h
            calculated_width = math.ceil(k * w)
            image_resize = cv2.resize(image_crop, (calculated_width, image_size))
            image_resize_shape = image_resize.shape
            width_gap = math.ceil((image_size-calculated_width) / 2)
            image_white[:, width_gap:calculated_width + width_gap] = image_resize
            image_white_predict = np.expand_dims(image_white, axis=0)
            prediction = model.predict(image_white_predict)
            print(prediction)
            control_game(prediction)

        else:
            try:

                k = image_size / w
                calculated_height = math.ceil(k * h)
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



        cv2.imshow("ImageCrop", image_crop)
        cv2.imshow("ImageWhite", image_white)

    cv2.imshow("Image", image)
    # cv2.waitKey(1)
    key = cv2.waitKey(1)
    if key == ord("s"):
        counter += 1
        cv2.imwrite(f"{folder}/Image_{time.time()}.jpg", image_white)
        print(counter)
