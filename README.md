# Arabic Handwriting Recognition using Image Processing Techniques and CNN. 
This project aims to develop an Arabic handwriting recognition system by utilizing Convolutional Neural Networks (CNNs) and image processing techniques to segment each individual character from the input images.

# Image processing 

The preprocessed images were segmented into individual characters using image processing techniques such as binarization, morphological operations, and connected component analysis.

1- Gaussian Blur filter with kernel of (3,3) 

2-Binary threshold combined with otsu algorithm to get the optimal threshold value

![image](https://github.com/hosam00767/Arabic-HandWriting-Recognition/assets/48860916/8e5102cf-29b2-4073-a79d-6a6130277453)![image](https://github.com/hosam00767/Arabic-HandWriting-Recognition/assets/48860916/c33832b5-7e11-4ec0-aa3d-e8157b21355b)

```ruby
def preprocess(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gaussian = cv.GaussianBlur(gray, (v.BLUR_KERNEL_VALUE, v.BLUR_KERNEL_VALUE), 0)
    ret, thresh = cv.threshold(gaussian, v.THRESHOLD_VALUE, 255, cv.THRESH_BINARY_INV)
    return thresh
```
# Charachter segmentation
## 1. Image to lines

The horizontal projection  function will help us determine how many white pixel in each row of the image 
After getting the list of pixels number from the horizontal projection function we will loop through the them to determine the start and the end of each line then crop each line from the image saving each line in array of line and return it as output

![image](https://github.com/hosam00767/Arabic-HandWriting-Recognition/assets/48860916/67810d87-9a44-4b21-9970-d274f6b0f4a0)
![image](https://github.com/hosam00767/Arabic-HandWriting-Recognition/assets/48860916/684eef0d-c4d7-4354-bfc3-8db555f82c4a)

```ruby
def horizontal_proj(img):
    img = preprocess(img)
    thresh_line = img / 255
    hproj = np.sum(thresh_line, 1)
    hproj_img = np.zeros((thresh_line.shape[0], thresh_line.shape[1]))
    for row in range(thresh_line.shape[0]):
        cv.line(hproj_img, (0, row), (int(hproj[row]), row), (255, 255, 255), 1)

    return hproj_img, hproj
```

## 2. Lines to (part of words) PAWS
   we extracted every connected component from the line to solve the issue of the overlapping characters and then we started to associate each point to the nearest compoment

![image](https://github.com/hosam00767/Arabic-HandWriting-Recognition/assets/48860916/b7647e2d-c334-4473-acc0-719f69b79865)
![image](https://github.com/hosam00767/Arabic-HandWriting-Recognition/assets/48860916/dfc5e219-11ea-4810-ad33-3eb3300cd78c)

## 3. Paws to characters 
in this phase we created the vertical projection vector of the image and segement each character with respect to the dots.

![image](https://github.com/hosam00767/Arabic-HandWriting-Recognition/assets/48860916/d3430d0d-4412-4a54-8e34-c5a5118e3773)
![image](https://github.com/hosam00767/Arabic-HandWriting-Recognition/assets/48860916/acfe60db-dd58-4ba1-bec3-a272244b1628)
```ruby
def vertical_proj(img):
    img = preprocess(img)
    thresh_line = img / 255
    vproj = np.sum(thresh_line, 0)
    vproj_img = np.zeros((thresh_line.shape[0], thresh_line.shape[1]))
    for col in range(thresh_line.shape[1]):
        cv.line(vproj_img, (col, thresh_line.shape[0]), (col, thresh_line.shape[0] - int(vproj[col])), (255, 255, 255),1)
    return vproj_img, vproj
```

# Challenges we faced and our solutions to it.
## 1. Skew Correction
Some time there is some skew in the word and it need some roation we develop a fuction that auto correct the skewness of the image.
![image](https://github.com/hosam00767/Arabic-HandWriting-Recognition/assets/48860916/271bd51d-bc3e-464a-b4f5-b1be7fae96de)

This How our function works : 
1. This function in an implementation of Projection Profile Method algorithm for skew 
angle estimation
2. It Rotates the image with a range of angels (-30,30) using the Transformation 
matrix.
3. For each rotation it calculate the horizontal projection and calculates a score for 
that horizontal projection 
4. The histogram with the highest score is the skewed histogram of the image and we 
save the rotation by that value

```ruby
def correct_skew(image, delta=1, limit=15):
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
```
## 2. Segmenting with respect to the dots

We we tried to segemnt the image without putting into considration the dots the Output of the segmention process wasn't great
![image](https://github.com/hosam00767/Arabic-HandWriting-Recognition/assets/48860916/0c5c935d-ca86-409f-b0a3-b232457e78fe)

So we decided to put into consideration the location of the dot we segement the charatchers

## 3. Segmenting the overlapping PAWS

We we detected each connected component and assign to it each dot after that we try to segement it we will face an issue the other connected componeent is overlapping with it

![image](https://github.com/hosam00767/Arabic-HandWriting-Recognition/assets/48860916/e5c07ce9-6694-4487-a17c-318d460c94d1)

Our soloution to that problem was to completly change the color of the other  connected compented to the white color as it will be completely removed when we make the image binary

![image](https://github.com/hosam00767/Arabic-HandWriting-Recognition/assets/48860916/2b956ee1-a46d-4416-9781-824afdca6edf)



# Dataset
We used the HMBD V1 dataset which contains a total number of 54,115 handwritten Arabic words,The HMBD dataset captures the different positions of the Arabic handwritten characters; isolated, beginning, middle, and end.
https://www.kaggle.com/datasets/hossammbalaha/hmbd-v1-arabic-handwritten-characters-dataset


# Convolutional Neural Network
We trained a CNN model using TensorFlow to classify each segmented character into one of the 28 Arabic letters or one of the 3 diacritics. The model achieved an accuracy of 92.5% on the test set. 


![image](https://github.com/hosam00767/Arabic-HandWriting-Recognition/assets/48860916/4e0f085d-a283-4007-b031-5a039d3ad9e6) 



# Requirements
Python 3.6 or higher
TensorFlow 2.0 or higher
OpenCV
Numpy
Usage
Clone the repository
Install the required dependencies
Run python predict.py <path_to_image> to predict the characters in the given image.

# Results
The model was able to accurately classify the majority of the characters in the test set. However, there were some cases where the model struggled to correctly classify characters due to variations in handwriting styles and the presence of noise in the input images.

# Future Work
We plan to further improve the accuracy of the model by incorporating more advanced image processing techniques and exploring other deep learning architectures. We also plan to expand the dataset to include more diverse handwriting styles and diacritics.

# Acknowledgements
We would like to thank the creators of the IFN/ENIT dataset for providing us with a high-quality dataset to work with. We would also like to thank the TensorFlow and OpenCV communities for their contributions to the field of deep learning and computer vision.
