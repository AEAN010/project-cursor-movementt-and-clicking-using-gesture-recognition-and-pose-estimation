# -*- coding: utf-8 -*-
"""
Created on Fri May 24 11:27:49 2024

@author: Anand
"""

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

def create_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(300, 300, 1)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(3, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model


import cv2
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import numpy as np



def preprocess_images(image_paths):
    data_list = []
    for img_path in image_paths:
        image = cv2.imread(img_path)
        
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_norm = gray_image / 255
        data_list.append(gray_norm)
    return data_list



path = r"C:\Users\Anand\internship_project\pose_estimationusingmediapipe\model_gesture\pose_gesture"
image_path = []

for folder in os.listdir(path):
    folder_path = os.path.join(path, folder)
    if os.path.isdir(folder_path):
        for img in os.listdir(folder_path):
            img_path = os.path.join(folder_path, img)
            image_path.append(img_path)
            
       


paper = 907
rock = 907
scissor = 903
labels = [0] * paper + [1] * scissor + [2] * rock

data = list(zip(image_path, labels))
np.random.shuffle(data)

X, Y = zip(*data)

data_x = preprocess_images(X)
data_y = Y

X_train, X_test, y_train, y_test = train_test_split(np.array(data_x),np.array( data_y), test_size=0.2, random_state=42)

model = create_model()
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Visualize training history
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()



path=r"C:/Users/Anand/internship_project/pose_estimationusingmediapipe/model_gesture/pose_gesture/scissor/scissors_3.png"


img_test=preprocess_images([path])
res=model.predict(np.array(img_test))
print((res))

from tensorflow.keras.models import load_model
model.save("trained_pose_gesture.h5")