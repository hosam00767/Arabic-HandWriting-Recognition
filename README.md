# Arabic Handwriting Recognition using Image Processing Techniques and CNN. 
This project aims to develop an Arabic handwriting recognition system by utilizing Convolutional Neural Networks (CNNs) and image processing techniques to segment each individual character from the input images.

# Image processing 

The preprocessed images were segmented into individual characters using image processing techniques such as binarization, morphological operations, and connected component analysis.

1- Gaussian Blur filter with kernel of (3,3) 

2-Binary threshold combined with otsu algorithm to get the optimal threshold value

![image](https://github.com/hosam00767/Arabic-HandWriting-Recognition/assets/48860916/8e5102cf-29b2-4073-a79d-6a6130277453)![image](https://github.com/hosam00767/Arabic-HandWriting-Recognition/assets/48860916/c33832b5-7e11-4ec0-aa3d-e8157b21355b)

# Charachter segmentation
1. The horizontal projection  function will help us determine how many white pixel in each row of the image 
After getting the list of pixels number from the horizontal projection function we will loop through the them to determine the start and the end of each line then crop each line from the image saving each line in array of line and return it as output

![image](https://github.com/hosam00767/Arabic-HandWriting-Recognition/assets/48860916/67810d87-9a44-4b21-9970-d274f6b0f4a0)
![image](https://github.com/hosam00767/Arabic-HandWriting-Recognition/assets/48860916/684eef0d-c4d7-4354-bfc3-8db555f82c4a)



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
