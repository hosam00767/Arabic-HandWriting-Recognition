# remover the noise by blurring the image and then do a threshold with a certain value to only show the writings
import cv2 as cv
import numpy as np

from .ImageValues import Values as v


def preprocess(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gaussian = cv.GaussianBlur(gray, (v.BLUR_KERNEL_VALUE, v.BLUR_KERNEL_VALUE), 0)
    ret, thresh = cv.threshold(gaussian, v.THRESHOLD_VALUE, 255, cv.THRESH_BINARY_INV)
    return thresh


def thining(img):
    x = preprocess(img)
    return cv.ximgproc.thinning(x, )


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv.INTER_LINEAR, borderValue=(255, 255, 255))
    return result


def edit_preprocessing_values(img):
    dots=[]
    thresh = preprocess(img)
    contours, _ = cv.findContours(image=thresh, mode=cv.RETR_CCOMP, method=cv.CHAIN_APPROX_NONE)
    coloredImage = cv.cvtColor(thresh, cv.COLOR_GRAY2BGR)
    for cnt in contours:

        if 3 < cv.contourArea(cnt) < v.DOT_AREA_VALUE:
            dots.append(cnt)
    if len(dots)>0:
        cv.fillPoly(coloredImage, pts=dots, color=(255, 0, 255))
    return coloredImage


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
        cv.line(vproj_img, (col, thresh_line.shape[0]), (col, thresh_line.shape[0] - int(vproj[col])), (255, 255, 255),1)
    return vproj_img, vproj
