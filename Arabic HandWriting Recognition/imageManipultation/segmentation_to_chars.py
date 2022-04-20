# segments the words into character based on the baseline of that word
from .preprocessing import *


def segment_to_chars(img):
    hproj, _ = horizontal_proj(img)
    srows = np.sum(hproj, 1)
    baseline = np.max(srows)
    baseline_index = np.where(srows == baseline)
    x = int(baseline_index[0][0])

    imupbl = img[0:x - 1, :]

    vimupbl, vproj = vertical_proj(imupbl)

    flag = True
    left = []
    right = []

    for i in range(img.shape[1]):

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
    points = []
    list(points)
    for i in range(len(left)):
        points.append(int((right[i] + left[i]) / 2))

    for i in range(len(points)):
        if i == 0:
            segmented_char = img[0:, 0:points[i]]

        else:
            segmented_char = img[0:, points[i - 1]:points[i]]

        cv.imwrite(r'images/chars/' + "char " + str(i) + "-line " + ".png", segmented_char)
