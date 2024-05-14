import time
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("Model/hand_gesture_model.keras", "Model/labels.txt")

offset = 40
image_size = 300

folder = "Data/IV"
counter = 0

labels = ["I", "II", "III", "IV"]

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
            cv2.imshow("ImageWhite", image_white)
            prediction, index = classifier.getPrediction(image)
            print(prediction, index)
        else:
            try:

                k = image_size / w
                calculated_height = math.ceil(k * h)
                image_resize = cv2.resize(image_crop, (calculated_height, image_size))
                image_resize_shape = image_resize.shape
                height_gap = math.ceil((image_size-calculated_height) / 2)
                image_white[height_gap:calculated_height + height_gap, :] = image_resize
                cv2.imshow("ImageWhite", image_white)
            except:
                print("can't fit an image")

        cv2.imshow("ImageCrop", image_crop)

    cv2.imshow("Image", image)
    cv2.waitKey(1)
    # key = cv2.waitKey(1)
    # if key == ord("s"):
    #     counter += 1
    #     cv2.imwrite(f"{folder}/Image_{time.time()}.jpg", image_white)
    #     print(counter)
