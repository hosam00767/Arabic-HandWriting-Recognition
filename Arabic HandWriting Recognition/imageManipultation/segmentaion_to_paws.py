import math
from .preprocessing import *


def distance(p1, p2):
    return math.sqrt(((p1[0] - p2[0][0]) ** 2) + ((p1[1] - p2[0][1]) ** 2))


def check_for_inter(dot, not_dot):
    x1, _, w1, _ = cv.boundingRect(dot)
    x2, _, w2, _ = cv.boundingRect(not_dot)
    if x1 in range(x2, x2 + w2) or x1 + w1 in range(x2, x2 + w2):
        return True
    else:
        return False


def sort_contours(cnts):
    boundingBoxes = [cv.boundingRect(c) for c in cnts]
    cnts, _ = zip(*sorted(zip(cnts, boundingBoxes), key=lambda b: b[1][0], reverse=True))
    return cnts


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


def segment_img_to_PAWS(path, lineNo, dotArea):
    img = cv.imread(path)
    dots = []
    component = []
    p = preprocess(img)
    contours, _ = cv.findContours(image=p, mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_NONE)

    for cnt in contours:
        if cv.contourArea(cnt) < dotArea:
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


def extract(img, component, lineNo):
    for i in range(len(component)):
        mask = zero = np.ones_like(img) * 255
        hull = cv.convexHull(component[i])
        cv.drawContours(mask, [hull], -1, (0, 0, 0), -1)
        cv.drawContours(mask, [hull], -1, (0, 0, 0), 5)
        zero[mask == (0, 0, 0)] = img[mask == (0, 0, 0)]
        zero = trim(zero)
        cv.imwrite(r'images/paws/' + str(lineNo) + str(i) + ".png", zero)


def trim(paw):
    _, vproj = vertical_proj(paw)
    left = []
    right = []
    flag = True
    for i in range(paw.shape[1]):
        cnt = 0
        if flag:
            cnt = vproj[i]
            if cnt > 0:
                left = i
                flag = False
        else:
            cnt = vproj[i]
            if cnt < 2:
                right = i
                flag = True

    if right is None:
        right = vproj.shape[1]

    timg = paw[0:, left - 4:right + 4]

    return timg
