import os
import glob as gb
import cv2
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelBinarizer
import imgaug.augmenters as iaa

#  Image Augmentation
augmentation = iaa.Sequential([
     iaa.Affine(
               rotate=(-10, 10),
               scale=(0.5, 1.5)  
                ) ])


#function to prepare the data set
def prepare_dataset(path,img_array,label_array,data_augmentation=False):
    for folder in  os.listdir(path) : 
        files = gb.glob(pathname= str( path +'/' + folder + '/*.jpg'))
        images_aug=[] 
        for file in files: 
            image = cv2.imread(file,0)
            gaussian = cv2.GaussianBlur(image, (5, 5), 0)
            _, thresh = cv2.threshold(gaussian, 92, 256, cv2.THRESH_BINARY_INV)
            normalized_img =thresh/255
            new_img = cv2.resize(normalized_img, (width,height))
            if data_augmentation:
                images_aug.append(new_img)
            img_array.append(list(new_img))
            label_array.append(classes_dict[folder])
        if data_augmentation:
            new_aug=[]
            for i in range(2):
                new_aug+=images_aug
            augmented_images = augmentation(images=new_aug)
            for img in augmented_images:
                img_array.append(list(img))
                label_array.append(classes_dict[folder])
        
    

train_path = 'dataset/train'
val_path = 'dataset/val'
test_path = 'dataset/test'


width=height=64



#getting data from directory apply preprocessing techniques and saving result in arrays

#preprocessing the train data with data augmentation
X_train = []
y_train = []
prepare_dataset(train_path,X_train,y_train,True)

#preproccing for validation data
X_val = []
y_val = []
prepare_dataset(val_path,X_val,y_val) 

#making data suitable for model training
X_train = np.array(X_train)
X_val = np.array(X_val)
y_train = np.array(y_train)
y_val = np.array(y_val)
train_y_labels = LabelBinarizer().fit_transform(y_train)
val_y_labels = LabelBinarizer().fit_transform(y_val)
