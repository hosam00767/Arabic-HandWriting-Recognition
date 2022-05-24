import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os
from .classes_info import *



# making a dictionary out of my classes to hold names and indexes
global classes_dict
classes_dict = {}
for i in range(len(classes)):
    classes_dict[classes[i]] = i


# gets the name of my class
def getclass(n):
    for x, y in classes_dict.items():
        if n == y:
            return x

        # function to resize the images to fit the model


def resize_image(img, size=(64, 64)):
    h, w = img.shape[:2]
    c = img.shape[2] if len(img.shape) > 2 else 1

    if h == w:
        return cv2.resize(img, size, cv2.INTER_AREA)

    dif = h if h > w else w

    interpolation = cv2.INTER_AREA if dif > (size[0] + size[1]) // 2 else cv2.INTER_CUBIC

    x_pos = (dif - w) // 2
    y_pos = (dif - h) // 2

    if len(img.shape) == 2:
        mask = 255 * np.ones((dif, dif), dtype=img.dtype)
        mask[y_pos:y_pos + h, x_pos:x_pos + w] = img[:h, :w]
    else:
        mask = 255 * np.ones((dif, dif, c), dtype=img.dtype)
        mask[y_pos:y_pos + h, x_pos:x_pos + w, :] = img[:h, :w, :]

    return cv2.resize(mask, size, interpolation)


# function predict characters, given the lines directory and a model directory,
# and returning a doc array of arrays representing each line
def predict_(dire,KERNEL_VALUE,THRESHOLD_VALUE, model="model/7model18.h5"):
    my_model = load_model(model)
    l = 0
    lines = len(os.listdir(dire))
    doc = []

    for i in range(lines):
        doc.append([])
    for line in os.listdir(dire):
        w = 0
        num_words = len(os.listdir(dire + '/' + line))
        for i in range(num_words):
            doc[l].append("")
        for word in range(len(os.listdir(dire + '/' + line))):
            chars = []
            for char in os.listdir(dire + '/' + line + '/' + "paw " + str(word)):
                image = cv2.imread(dire + '/' + line + '/' + "paw " + str(word) + '/' + char, 0)
                image = resize_image(image)
                gaussian = cv2.GaussianBlur(image, (KERNEL_VALUE, KERNEL_VALUE), 0)
                _, thresh = cv2.threshold(gaussian, THRESHOLD_VALUE, 255, cv2.THRESH_BINARY_INV)
                new_img = thresh / 255
                img = np.expand_dims(new_img, axis=0)
                chars.append(img)
            # reverse chars order
            for char in range(len(chars) - 1, -1, -1):
                prediction = my_model.predict(chars[char])
                doc[l][w] += get_char(np.argmax(prediction))
                #####################################################################
            w += 1
            #########################################################################
        l += 1
        #############################################################################
    return doc
