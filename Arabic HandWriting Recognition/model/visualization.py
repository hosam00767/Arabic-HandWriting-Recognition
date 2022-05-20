import cv2
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential,Model,load_model
import os
import matplotlib.pyplot as plt
import glob as gb
from .classes_info import *
from .prediction import resize_image , getclass

#loading model
model = load_model("7model18.h5")

# loading model history
history=np.load("7model18.npy",allow_pickle='TRUE').item()

#ploting model (validation and train) accuracy
plt.plot(history['accuracy'])
plt.plot(history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epochs')
plt.legend(['validation','train'],loc='upper left')
plt.show()

#ploting model (validation and train) loss
plt.plot(history['val_loss'])
plt.plot(history['loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epochs')
plt.legend(['validation','train'],loc='upper left')
plt.show()

###############################################################################
#plotting the model result on test data
test_path = 'dataset/test'
X_pred = []
for folder in  os.listdir(test_path) : 
    files = gb.glob(pathname= str( test_path +'/' + folder + '/*.jpg'))
    for file in files: 
        image = cv2.imread(file,0)
        image=resize_image(image)
        gaussian = cv2.GaussianBlur(image, (5, 5), 0)
        _, thresh = cv2.threshold(gaussian, 92, 256, cv2.THRESH_BINARY_INV)
        new_img=thresh/255
        X_pred.append(list(new_img))
X_pred_array=np.array(X_pred)

y_result = model.predict(X_pred_array)

#plotting random images with their result
plt.figure(figsize=(20,20))
for n , i in enumerate(list(np.random.randint(0,len(X_pred),36))) : 
    plt.subplot(6,6,n+1)
    plt.imshow(X_pred[i])    
    plt.axis('off')
    plt.title(getclass(np.argmax(y_result[i])))




