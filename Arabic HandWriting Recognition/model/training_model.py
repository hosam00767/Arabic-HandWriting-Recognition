import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping,ReduceLROnPlateau
from tensorflow.keras.layers import Input, Dense, Activation, Flatten, Conv2D, MaxPool2D, Dropout,BatchNormalization
from tensorflow.keras.models import Sequential,Model
from tensorflow.keras.optimizers import Adam 
from .dataset_preprocessing import *


# Input layer
input_img = Input(shape  = (width,height,1), name = 'img_input')

# Convo layers
x = Conv2D(64, (3,3) , padding = 'same' , activation='relu', name = 'layer_1') (input_img)
x = MaxPool2D((2,2), name = 'layer_2') (x)
x = Dropout(0.25) (x)
x = Conv2D(128, (3,3) , padding = 'same' , activation='relu', name = 'layer_3') (x)
x = MaxPool2D((2,2), name = 'layer_4') (x)
x = Dropout(0.25) (x)
x = Conv2D(256, (3,3) , padding = 'same' , activation='relu', name = 'layer_5') (x)
x = MaxPool2D((2,2), name = 'layer_6') (x)
x = Dropout(0.25) (x)
x = Flatten()(x)
x= Dense(1024, name = 'layer_7')(x)
x= Dense(512, name = 'layer_8')(x)
x = Dropout(0.5) (x)
x = Dense(105, activation='softmax', name='predictions')(x)

# # Generate the model
my_model = Model(inputs = input_img, outputs =x , name='chars_classification' )

# # Print network structure
my_model.summary()


#stops when there's no improvement in validation loss for 3 epochs
early_stopping=EarlyStopping( monitor="val_loss", patience=3,
                                     verbose=1,  restore_best_weights=True)


#reduces learning rate when there's no improvement in validation loss for 1 epochs
reduce_lr=ReduceLROnPlateau( monitor="val_loss", factor=0.5, patience=1,
                                             verbose=1)


BATCH_SIZE=256

# to ensure that there are enough images for training and validation batches
TRAIN_STEPS_PER_EPOCH = np.ceil((len(X_train)*0.8/BATCH_SIZE)-1)
VAL_STEPS_PER_EPOCH = np.ceil((len(X_val)*0.2/BATCH_SIZE)-1)

#compiling the model
my_model.compile(optimizer ='adam',loss='categorical_crossentropy',metrics=['accuracy'])

#start the training
history=my_model.fit(X_train,train_y_labels,
    steps_per_epoch=TRAIN_STEPS_PER_EPOCH,
    validation_data=(X_val,val_y_labels),
    validation_steps=VAL_STEPS_PER_EPOCH,
    epochs=25,callbacks=[ reduce_lr , early_stopping])



