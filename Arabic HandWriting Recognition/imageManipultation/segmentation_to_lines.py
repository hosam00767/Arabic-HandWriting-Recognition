import cv2 as cv
import cv2 as cv
from .preprocessing import *
import os
import shutil


# segments an image to line  based of the horizontal projection of the line pixels
def segment_to_line(img):
    if os.path.exists("images/lines"):
        shutil.rmtree("images/lines", ignore_errors=True)
    os.mkdir("images/lines")

    if os.path.exists("images/linez"):
        shutil.rmtree("images/linez", ignore_errors=True)
        os.mkdir("images/linez")
    else:
        os.mkdir("images/linez")

    if os.path.exists("images/paws"):
        shutil.rmtree("images/paws", ignore_errors=True)
        os.mkdir("images/paws")
    else:
        os.mkdir("images/paws")

    if os.path.exists("images/chars"):
        shutil.rmtree("images/chars", ignore_errors=True)
        os.mkdir("images/chars")
    else:
        os.mkdir("images/chars")

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

        if timg.shape[0] > 12:
            text_lines.append(timg)

    for i in range(len(text_lines)):
        cv.imwrite("images/lines/" + str(i) + ".png", text_lines[i])
        os.mkdir("images/linez/line " + str(i))