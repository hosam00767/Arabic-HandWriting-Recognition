# remover the noise by blurring the image and then do a threshold with a certain value to only show the writings
import cv2 as cv
import numpy as np
def preprocess(img,x):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gaussian = cv.GaussianBlur(gray, (5, 5), 0)
    ret, thresh = cv.threshold(gaussian, x, 255, cv.THRESH_BINARY_INV)

    return thresh


