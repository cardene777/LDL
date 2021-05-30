import glob
import os

import cv2
import numpy as np
from keras.callbacks import TensorBoard
from keras.utils import to_categorical

from models import VGG16

DATA_DIR = "data"
LOGS_DIR = os.path.join("logs", "vgg16")

classes = ["person", "cat", "dog"]

model = VGG16(gpus=4)
input_H, input_W = model.input.shape[1:3]

images = {}
labels = {}

for mode in ["train", "valid"]:
    images[mode] = []
    labels[mode] = []
    for class_index, class_name in enumerate(classes):
        files = glob.glob(os.path.join(DATA_DIR, mode, class_name, "*.jpg"))
        for file_path in files:
            img = cv2.imread(file_path)
            img = cv2.resize(img, (input_W, input_H))
            img = img / 255
            images[mode].append(img)
            labels[mode].append(
                to_categorical(class_index, num_classes=len(classes))
            )
    images[mode] = np.array(images[mode])
    labels[mode] = np.array(labels[mode])

tensorboard_callback = TensorBoard(log_dir=LOGS_DIR)
model.fit(
    images["train"],
    labels["train"],
    validation_data=(images["valid"], labels["valid"]),
    batch_size=256,
    epochs=200,
    callbacks=[tensorboard_callback]
)

model.save(os.path.join(
    "results",
    "vgg16_200epoch_lr0.01_3000images.h5"
))
