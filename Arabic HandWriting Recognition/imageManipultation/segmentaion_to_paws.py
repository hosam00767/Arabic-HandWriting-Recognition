import math
from .preprocessing import *
from .ImageValues import Values as v
import os

def getDistance(p1, p2):
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
def sort_contours(contoursList):
    boundingBoxes = [cv.boundingRect(c) for c in contoursList]
    sortedContoursList = sorted(contoursList, key=lambda cnt: getPawStartIndex(cnt), reverse=True)
    return sortedContoursList


def shortest_distance(cnt1, dot):
    x, y, w, h = cv.boundingRect(dot)
    dist = 9999999

    for n in cnt1:
        if getDistance((x, y), n) <= dist:
            dist = getDistance((x, y), n)
    return dist


def mergeContours(ctrs_to_merge):
    list_of_pts = []
    for ctr in ctrs_to_merge:
        list_of_pts += [pt[0] for pt in ctr]
    ctr = np.array(list_of_pts).reshape((-1, 1, 2)).astype(np.int32)
    return ctr


def getTheNearestContour(listOfContours, dot):
    nearestContour = listOfContours[0]
    nearestDistance = shortest_distance(listOfContours[0], dot)

    for contour in listOfContours:
        distance = shortest_distance(contour, dot)
        if nearestDistance > distance:
            nearestDistance = distance
            nearestContour = contour

    return listOfContours.index(nearestContour)


def getIndexOfObjectInList(contourList, contourObject):
    for i, listObject in enumerate(contourList):
        if listObject is contourObject:
            indexOfThePaw = i
    return indexOfThePaw


def segment_img_to_PAWS(path, lineNo):
    img = cv.imread(path)
    listOFContoursOFDots = []
    listOfContoursOfPaws = []
    p = preprocess(img)
    contours, _ = cv.findContours(image=p, mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_NONE)

    # For Each Contour of The Image it check for its size for a certain area value
    for cnt in contours:
        if cv.contourArea(cnt) < v.DOT_AREA_VALUE:
            listOFContoursOFDots.append(cnt)  # If it less Than that Threshold Value it will be considered a dot
        else:
            listOfContoursOfPaws.append(cnt)  # If it  more Than that Threshold Value it will be considered a Paw

    # Sorting the contour base of the x value of their end
    listOfContoursOfPaws = sort_contours(listOfContoursOfPaws)
    listOfContoursOfPaws = list(listOfContoursOfPaws)

    # For each dot we got we check for its vertical intersection with the PAWs contours
    # save these intersected contours in a List
    for dot in listOFContoursOFDots:
        intersectedContoursList = []

        for cnt in listOfContoursOfPaws:
            if check_for_inter(dot, cnt):
                intersectedContoursList.append(cnt)
        list(intersectedContoursList)
        # If there is only one PAW is intersecting with the dot
        # we merge the contours of the dot and the Paw into one contour

        if len(intersectedContoursList) == 1:

            indexOfThePaw=getIndexOfObjectInList(listOfContoursOfPaws,intersectedContoursList[0])

            listOfContoursOfPaws[indexOfThePaw] = mergeContours([listOfContoursOfPaws[indexOfThePaw], dot])

        # If there is 2 PAWs are intersecting with the same dot
        # we find the closest paw to the dot and merge the paw and dot into one contour
        elif len(intersectedContoursList) == 2:
            firstIntersectedContour = intersectedContoursList[0]
            secondIntersectedContour = intersectedContoursList[1]

            distanceOfFirstContourAndDot = shortest_distance(firstIntersectedContour, dot)
            distanceOfSecondContourAndDot = shortest_distance(secondIntersectedContour, dot)

            if distanceOfFirstContourAndDot <= distanceOfSecondContourAndDot:
                indexOfThePaw = getIndexOfObjectInList(listOfContoursOfPaws, firstIntersectedContour)
                listOfContoursOfPaws[indexOfThePaw] = mergeContours(
                    [listOfContoursOfPaws[indexOfThePaw], dot])
            else:
                indexOfThePaw = getIndexOfObjectInList(listOfContoursOfPaws, secondIntersectedContour)
                listOfContoursOfPaws[indexOfThePaw] = mergeContours(
                    [listOfContoursOfPaws[indexOfThePaw], dot])

        # If there is no PAWs are intersecting with the dot
        elif len(intersectedContoursList) == 0:

            # if there is only one paw in the image
            # merge the dot with the paw
            if len(listOfContoursOfPaws) == 1:
                listOfContoursOfPaws[0] = mergeContours([listOfContoursOfPaws[0], dot])

            # if there is more than one paw in the image
            # merge the dot with the nearest paw to it
            elif len(listOfContoursOfPaws) > 1:
                shortestContourIndex = getTheNearestContour(listOfContoursOfPaws, dot)
                listOfContoursOfPaws[shortestContourIndex] = mergeContours(
                    [listOfContoursOfPaws[shortestContourIndex], dot])

    extract(img, listOfContoursOfPaws, lineNo)


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

        if zero.shape[0] * zero.shape[1] > 15:
            cv.imwrite(r'images/paws/' + "paw " + str(i) + "_line " + str(lineNo) + ".png", zero)
            os.mkdir("images/linez/line "+str(lineNo)+"/paw "+str(i))