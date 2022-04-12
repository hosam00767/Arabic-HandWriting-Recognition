import cv2 as cv
from .preprocessing import *


# segments an image to line  based of the horizontal projection of the line pixels
def segment_to_line(img):
    _, vproj = horizontal_proj(img)
    upper = []
    lower = []
    flag = True
    for i in range(vproj.shape[0]):
        cnt = 0
        if flag:
            cnt = vproj[i]
            if cnt > 0:
                upper.append(i)
                flag = False
        else:
            cnt = vproj[i]
            if cnt < 2:
                lower.append(i)
                flag = True
    text_lines = []

    if len(upper) != len(lower):
        lower.append(img.shape[0])

    for i in range(len(upper)):
        timg = img[upper[i] - 2:lower[i] + 2, 0:]

        if timg.shape[0] > 6:
            text_lines.append(timg)

    for i in range(len(text_lines)):
        cv.imwrite("images/lines/" + str(i) + ".png", text_lines[i])
