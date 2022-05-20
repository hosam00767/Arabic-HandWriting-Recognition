import os
import glob as gb
import cv2
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelBinarizer

train_path = 'dataset/train'
val_path = 'dataset/val'
test_path = 'dataset/test'

width=height=64

X_train = []
y_train = []

#getting data from directory apply preprocessing techniques and saving result in arrays
for folder in  os.listdir(train_path) : 
    files = gb.glob(pathname= str( train_path +'/' + folder + '/*.jpg'))
    for file in files: 
        image = cv2.imread(file,0)
        gaussian = cv2.GaussianBlur(image, (5, 5), 0)
        _, thresh = cv2.threshold(gaussian, 92, 256, cv2.THRESH_BINARY_INV)
        normalized_img =thresh/255
        new_img = cv2.resize(normalized_img, (width,height))
        #train images
        X_train.append(list(new_img))
        #train labels
        y_train.append(classes_dict[folder])


#preproccing for validation data
X_val = []
y_val = []
for folder in  os.listdir(val_path) : 
    files = gb.glob(pathname= str( val_path +'/' + folder + '/*.jpg'))
    for file in files: 
        image = cv2.imread(file,0)
        gaussian = cv2.GaussianBlur(image, (5, 5), 0)
        _, thresh = cv2.threshold(gaussian, 92, 256, cv2.THRESH_BINARY_INV)
        normalized_img =thresh/255
        new_img = cv2.resize(normalized_img, (width,height))
        X_test.append(list(new_img))
        y_test.append(classes_dict[folder])

#making data suitable for model training
X_train = np.array(X_train)
X_val = np.array(X_val)
y_train = np.array(y_train)
y_val = np.array(y_val)
train_y_labels = LabelBinarizer().fit_transform(y_train)
val_y_labels = LabelBinarizer().fit_transform(y_val)
