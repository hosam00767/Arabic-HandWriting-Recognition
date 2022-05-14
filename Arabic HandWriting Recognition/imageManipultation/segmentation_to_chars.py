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

    return rotated


def remove_baseline(img):
    p = preprocess(img)
    hproj, _ = horizontal_proj(img)
    srows = np.sum(hproj, 1)

    baseline = np.max(srows)
    baseline_index = np.where(srows == baseline)
    x = int(baseline_index[0][0])
    for i in range(x - 2, x + 4):
        cv.line(img, (0, i), (img.shape[1], i), (255, 255, 255), 1)
    return img


# Remove the dots from a colored image
def remove_dots(img):
    preprocessedImg = preprocess(img)
    contours, _ = cv.findContours(image=preprocessedImg, mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        if cv.contourArea(cnt) < 35:
            cv.drawContours(img, cnt, -1, (255, 255, 255), -1)
    return img


def segment_to_chars(path, pawName):
    img = cv.imread(path)
    noDotsImg = remove_dots(img.copy())
    rotated = correct_skew(noDotsImg)
    noBaseLine = remove_baseline(rotated)
    print(path)
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
    points = [0]
    list(points)
    for i in range(len(left)):
        points.append(int((right[i] + left[i]) / 2))
    points.append(img.shape[1])

    for i in range(len(points) - 1):
        segmented_char = img[:, points[i]:points[i + 1]]

        if segmented_char.shape[1] * segmented_char.shape[0] > 15:
            cv.imwrite(r'images/chars/' + "char " + str(i) + '_' + pawName + ".png", segmented_char)
