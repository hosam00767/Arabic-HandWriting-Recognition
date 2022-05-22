# segments the words into character based on the baseline of that word
import copy
import cv2
import numpy
from .preprocessing import *
from scipy.ndimage import interpolation as inter


# ROTATES THE PAW IMAGE AND CALCULATE ITS SCORE
#
# RETURN ONLY THE HIGHEST SCORE
def correct_skew(image, delta=1, limit=20):
    def determine_score(arr, angle):
        data = inter.rotate(arr, angle, reshape=False, order=0)
        histogram = np.sum(data, axis=1)
        score = np.sum((histogram[1:] - histogram[:-1]) ** 2)
        return histogram, score

    thresh = preprocess(image)

    scores = []
    angles = np.arange(-limit, limit + delta, delta)
    for angle in angles:
        histogram, score = determine_score(thresh, angle)

        scores.append(score)

    best_angle = angles[scores.index(max(scores))]

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    M = cv.getRotationMatrix2D(center, best_angle, 1.0)
    rotated = cv.warpAffine(image, M, (w, h), flags=cv.INTER_CUBIC, borderValue=(255, 255, 255))
    return rotated


# return vector of the vertical projection that doesn't contain baseline
def removeBaseLine(img):
    x, vector = vertical_proj(img)
    maxBaseLineValue = int(numpy.mean(vector)*0.5)

    vector = removeFromEachIndex(copy.copy(vector), maxBaseLineValue)

    return vector


def removeFromEachIndex(vector, value):
    for i in range(vector.shape[0]):
        vector[i] = vector[i] - value
        if vector[i] < 0:
            vector[i] = 0
    return vector


# Remove the dots from a colored image
def remove_dots(img):
    dots = []
    preprocessedImg = preprocess(img)
    contours, _ = cv.findContours(image=preprocessedImg, mode=cv2.RETR_CCOMP, method=cv.CHAIN_APPROX_NONE)
    for cnt in contours:

        if 3 < cv.contourArea(cnt) < v.DOT_AREA_VALUE:
            dots.append(cnt)
    if len(dots) > 0:
        cv2.fillPoly(img, pts=dots, color=(255, 255, 255))

    return img


def check_for_inter(dot, left, right):
    x, _, width, _ = cv.boundingRect(dot)

    if x in range(left, right) or x + width in range(left, right):
        return True
    else:
        return False


def getTheDotOnTheLeft(dots):
    left, _, _, _ = cv.boundingRect(dots[0])
    for dot in dots:
        x, _, _, _ = cv.boundingRect(dot)
        if left > x:
            left = x
    return left


def segment_to_chars(path, pawName):
    dots = []
    img = cv.imread(path)
    contours, _ = cv.findContours(image=preprocess(img), mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        if cv.contourArea(cnt) < v.DOT_AREA_VALUE:
            dots.append(cnt)

    img = correct_skew(img)

    noDotsImg = remove_dots(img.copy())
    flag = True
    left = []
    right = []
    vproj = removeBaseLine(noDotsImg)

    for i in range(len(vproj)):
        cnt = 0
        if flag:
            cnt = vproj[i]
            if cnt == 0:
                left.append(i)
                flag = False
        else:
            cnt = vproj[i]
            if cnt > 1:
                right.append(i)
                flag = True

    if len(left) != len(right):
        right.append(img.shape[1])

    points = [0]
    list(points)
    intersectedDots = []
    for i in range(len(left)):
        for dot in dots:

            if check_for_inter(dot, left[i], right[i]):
                intersectedDots.append(dot)

        if len(intersectedDots) > 1:
            dotOnTheLeftIndex = getTheDotOnTheLeft(intersectedDots)
            points.append(int((dotOnTheLeftIndex + left[i]) / 2))

        elif len(intersectedDots) == 1:
            x, _, _, _ = cv.boundingRect(intersectedDots[0])
            points.append(int((x + left[i]) / 2))

        elif len(intersectedDots) == 0:

            if len(left) != 0:
                points.append(int((right[i] + left[i]) / 2))

    points.append(img.shape[1])

    for i in range(len(points) - 1):
        segmented_char = img[:, points[i]:points[i + 1]]

        if segmented_char.shape[1] * segmented_char.shape[0] > 15 and segmented_char.shape[1] > 5 and \
                segmented_char.shape[0] > 5:
            cv.imwrite(r'images/chars/' + "char " + str(i) + '_' + pawName + ".png", segmented_char)
            cv.imwrite(r'images/linez/' + pawName[pawName.index('_')+1:] +'/'+pawName[:pawName.index('_')]+'/'+ str(i) +".png", segmented_char)
