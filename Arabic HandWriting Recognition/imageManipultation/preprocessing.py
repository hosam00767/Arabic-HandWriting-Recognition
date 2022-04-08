# remover the noise by blurring the image and then do a threshold with a certain value to only show the writings
import cv2 as cv
import numpy as np
def preprocess(img,x):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gaussian = cv.GaussianBlur(gray, (5, 5), 0)
    ret, thresh = cv.threshold(gaussian, x, 255, cv.THRESH_BINARY_INV)

    return thresh


def horizontal_proj(img):
    img = preprocess(img)
    thresh_line = img / 255
    hproj = np.sum(thresh_line, 1)
    hproj_img = np.zeros((thresh_line.shape[0], thresh_line.shape[1]))
    for row in range(thresh_line.shape[0]):
        cv.line(hproj_img, (0, row), (int(hproj[row]), row), (255, 255, 255), 1)

    return hproj_img, hproj


def vertical_proj(img):
    img = preprocess(img)
    thresh_line = img / 255
    vproj = np.sum(thresh_line, 0)
    vproj_img = np.zeros((thresh_line.shape[0], thresh_line.shape[1]))
    for col in range(thresh_line.shape[1]):
        cv.line(vproj_img, (col, thresh_line.shape[0]), (col, thresh_line.shape[0] - int(vproj[col])), (255, 255, 255),
                1)
    return vproj_img, vproj

# stack images with same width vertically
def vconcat_resize_min(im_list, interpolation=cv.INTER_CUBIC):
    w_min = min(im.shape[1] for im in im_list)
    im_list_resize = [cv.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])), interpolation=interpolation)
                      for im in im_list]
    return cv.vconcat(im_list_resize)


# returns a preprocessed image that 3 channels image that each dot of that image is painted in white for not being
# detected in the preprocessing
def remove_dots(img):
    without_dots = img.copy()
    preprocessed = preprocess(img)
    contours, _ = cv.findContours(image=preprocessed, mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        if cv.contourArea(cnt) < 35:
            cv.drawContours(without_dots, cnt, -1, (255, 255, 255), 2)
    return without_dots
