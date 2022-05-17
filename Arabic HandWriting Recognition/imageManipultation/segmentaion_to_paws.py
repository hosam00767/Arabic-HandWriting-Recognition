import math
from .preprocessing import *
from .ImageValues import Values as v


# Takes a line path and its position in the image
# slice each set of contours in the image and saves it as png
def segment_img_to_PAWS(path, lineNo):
    img = cv.imread(path)
    dots = []
    component = []
    p = preprocess(img)
    contours, _ = cv.findContours(image=p, mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        if cv.contourArea(cnt) < v.DOT_AREA_VALUE:
            dots.append(cnt)
        else:
            component.append(cnt)
    component = sort_contours(component)
    component = list(component)

    for dot in dots:
        conflict = []
        for cnt in component:

            if check_for_inter(dot, cnt):
                conflict.append(cnt)

        if len(conflict) == 1:
            component[component.index(conflict[0])] = merge_ctrs([component[component.index(conflict[0])], dot])

        elif len(conflict) == 2:
            cnt1 = conflict[0]
            cnt2 = conflict[1]
            x1 = shortest_distance(cnt1, dot)
            x2 = shortest_distance(cnt2, dot)
            if x1 <= x2:
                component[component.index(cnt1)] = merge_ctrs([component[component.index(cnt1)], dot])
            else:
                component[component.index(cnt2)] = merge_ctrs([component[component.index(cnt2)], dot])

        # If the Dot don't overlap with any PAW
        elif len(conflict) == 0:
            print("not Yet Implement")

    extract(img, component, lineNo)


def distance(p1, p2):
    return math.sqrt(((p1[0] - p2[0][0]) ** 2) + ((p1[1] - p2[0][1]) ** 2))


def check_for_inter(dot, not_dot):
    x1, _, w1, _ = cv.boundingRect(dot)
    x2, _, w2, _ = cv.boundingRect(not_dot)
    if x1 in range(x2, x2 + w2) or x1 + w1 in range(x2, x2 + w2):
        return True
    else:
        return False


# Return the start position of a word from the x axis
def getPawStartIndex(cnt):
    x, _, w, _ = cv.boundingRect(cnt)
    return x + w


# Using a Lambda function(Sorted) to sort the Contours based of the the x axis
def sort_contours(cnts):
    boundingBoxes = [cv.boundingRect(c) for c in cnts]
    sortedCnts = sorted(cnts, key=lambda cnt: getPawStartIndex(cnt), reverse=True)
    return sortedCnts


def shortest_distance(cnt1, dot):
    x, y, w, h = cv.boundingRect(dot)
    dist = 9999999

    for n in cnt1:
        if distance((x, y), n) <= dist:
            dist = distance((x, y), n)
    return dist


def merge_ctrs(ctrs_to_merge):
    list_of_pts = []
    for ctr in ctrs_to_merge:
        list_of_pts += [pt[0] for pt in ctr]
    ctr = np.array(list_of_pts).reshape((-1, 1, 2)).astype(np.int32)
    return ctr


def segment_img_to_PAWS(path, lineNo):
    img = cv.imread(path)
    dots = []
    component = []
    p = preprocess(img)
    contours, _ = cv.findContours(image=p, mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        if cv.contourArea(cnt) < v.DOT_AREA_VALUE:
            dots.append(cnt)
        else:
            component.append(cnt)
    component = sort_contours(component)
    component = list(component)

    for dot in dots:
        conflict = []
        for cnt in component:

            if check_for_inter(dot, cnt):
                conflict.append(cnt)

        if len(conflict) == 1:
            component[component.index(conflict[0])] = merge_ctrs([component[component.index(conflict[0])], dot])

        elif len(conflict) == 2:
            cnt1 = conflict[0]
            cnt2 = conflict[1]
            x1 = shortest_distance(cnt1, dot)
            x2 = shortest_distance(cnt2, dot)
            if x1 <= x2:
                component[component.index(cnt1)] = merge_ctrs([component[component.index(cnt1)], dot])
            else:
                component[component.index(cnt2)] = merge_ctrs([component[component.index(cnt2)], dot])

    extract(img, component, lineNo)


def trim(paw):
    _, vproj = vertical_proj(paw)
    left = -1
    right = -1
    flag = True
    for i in range(paw.shape[1]):
        pixelsAtWidthI = 0
        if flag:
            pixelsAtWidthI = vproj[i]
            if pixelsAtWidthI > 0:
                left = i
                flag = False
        else:
            pixelsAtWidthI = vproj[i]
            if pixelsAtWidthI < 2:
                right = i
                flag = True
    # in case the contour did not end after the image width reached
    if right == -1:
        right = paw.shape[1]

    timg = paw[:, left:right]

    return timg


def extract(img, component, lineNo):
    for i in range(len(component)):
        mask = zero = np.ones_like(img) * 255
        hull = cv.convexHull(component[i])
        cv.drawContours(mask, [hull], -1, (0, 0, 0), -1)
        cv.drawContours(mask, [hull], -1, (0, 0, 0), 5)
        zero[mask == (0, 0, 0)] = img[mask == (0, 0, 0)]

        zero = trim(zero)

        if zero.shape[0]*zero.shape[1] > 15:
            cv.imwrite(r'images/paws/' + "paw " + str(i) + "_line " + str(lineNo) + ".png", zero)
