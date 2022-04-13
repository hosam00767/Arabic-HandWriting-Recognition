# segments the words into character based on the baseline of that word
def segment_to_chars(img):
    img = upper_histogram(img)
    _, vproj = vertical_proj(img)
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
    for i in range(len(left)):
        points.append(int((right[i] + left[i]) / 2))

    segmented_word = img.copy()
    print(points)
    for i in range(len(points)):
        cv.line(segmented_word, (points[i], 0), (points[i], segmented_word.shape[1]), (0, 0, 255), 1)
    return segmented_word
