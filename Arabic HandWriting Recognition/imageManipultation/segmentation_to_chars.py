# segments the words into character based on the baseline of that word
from .preprocessing import *
from scipy.ndimage import interpolation as inter


# ROTATES THE PAW IMAGE AND CALCULATE ITS SCORE
#
# RETURN ONLY THE HIGHEST SCORE
def correct_skew(image, delta=1, limit=30):
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

    return best_angle, rotated


def remove_baseline(img):
    skewed=correct_skew(img)
    hproj, _ = horizontal_proj(skewed)
    srows = np.sum(hproj, 1)

    baseline = np.max(srows)
    baseline_index = np.where(srows == baseline)
    x = int(baseline_index[0][0])
    for i in range(x - 2, x + 4):
        cv.line(img, (0, i), (img.shape[1], i), (255, 255, 255), 1)
    return img


def remove_dots(img):
    without_dots = img.copy()
    preprocessed = preprocess(img)
    contours, _ = cv.findContours(image=preprocessed, mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        if cv.contourArea(cnt) < 35:
            cv.drawContours(without_dots, cnt, -1, (255, 255, 255), 2)
    return without_dots


def segment_to_chars(img):
    noDots = remove_dots(img)
    noBaseLine = remove_baseline(noDots)
    angel, rotated = correct_skew(img)
    print(angel)
    cv.imshow("R", rotated)
    cv.waitKey(0)

    _, vproj = vertical_proj(noBaseLine)

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
