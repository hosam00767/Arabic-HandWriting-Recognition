import cv2
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential,Model,load_model
import os
import matplotlib.pyplot as plt
import glob as gb
import math
from mlxtend.plotting import plot_confusion_matrix
from sklearn.metrics import confusion_matrix
from sklearn.utils import shuffle
from .classes_info import *
from .prediction import resize_image , getclass



#loading model
model = load_model("model/model.h5")

# loading model history
history=np.load("model/model_history.npy",allow_pickle='TRUE').item()

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
test_path = 'dataset/test
width=height=64
X_test = []
y_test=[]
for folder in  os.listdir(test_path) : 
    files = gb.glob(pathname= str( test_path +'/' + folder + '/*.jpg'))
    for file in files: 
        image = cv2.imread(file,0)
        gaussian = cv2.GaussianBlur(image, (5, 5), 0)
        _, thresh = cv2.threshold(gaussian, 92, 256, cv2.THRESH_BINARY_INV)
        new_img=thresh/255
        new_img=cv2.resize(new_img,(width,height))
        X_test.append(list(new_img))
        y_test.append(classes_dict[folder])
X_test = np.array(X_test)
y_test = np.array(y_test)

y_result = model.predict(X_test)

#plotting random images with their result
plt.figure(figsize=(20,20))
for n , i in enumerate(list(np.random.randint(0,len(X_pred),36))) : 
    plt.subplot(6,6,n+1)
    plt.imshow(X_pred[i])    
    plt.axis('off')
    plt.title(getclass(np.argmax(y_result[i])))
#################################################################

#get the confusion matrix
test_labels, test_samples = shuffle(y_test, X_test)

predictions = model.predict(
      x=test_samples
    , batch_size=256
    , verbose=0
) 

rounded_predictions = np.argmax(predictions, axis=-1)

cm = confusion_matrix(y_true=test_labels, y_pred=rounded_predictions)

#get each class accuracy from the confusion matrix
classes_acc=cm.diagonal()/cm.sum(axis=1)

#sorting classes accuracy descending
classes_=classes

#function to get only two num after the dot in float numbers 
def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n

for i in range(len(classes_acc)):
    classes_acc[i]=truncate(classes_acc[i],3)

for i in range(len(classes_acc)):
    for j in range(len(classes_acc)):
        if float(classes_acc[i])>float(classes_acc[j]):
            temp=classes_acc[i]
            classes_acc[i]=classes_acc[j]
            classes_acc[j]=temp
            temp=classes_[i]
            classes_[i]=classes_[j]
            classes_[j]=temp
print(classes_acc)

#printing the results: each class accuracy percentage wit its name starting from the highest

for i in range(32):
    print(str(classes_[i])+" : "+str(int(round(classes_acc[i]/.01)))+"%")

