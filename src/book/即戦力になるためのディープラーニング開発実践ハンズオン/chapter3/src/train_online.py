import glob
import os

import cv2
import numpy as np
from keras.utils import to_categorical

from models import VGG16

DATA_DIR = "data"

classes = ["person", "cat", "dog"]

model = VGG16()
input_H, input_W = model.input.shape[1:3]

loss_history = open(os.path.join(
    "results",
    "vgg16_online_losses.csv"
), "w")

for _ in range(10):
    for class_index, class_name in enumerate(classes):
        files = glob.glob(os.path.join(DATA_DIR, "train", class_name, "*.jpg"))
        for file_path in files:
            img = cv2.imread(file_path)
            img = cv2.resize(img, (input_W, input_H))
            img = img / 255
            label = to_categorical(class_index, num_classes=len(classes))
            img = np.array([img])
            label = np.array([label])
            history = model.fit(img, label)
            loss_history.write(str(history.history["loss"][0]) + "\n")

loss_history.close()

model.save(os.path.join(
    "results",
    "vgg16_10epoch_lr0.01_30images_online.h5"
))
