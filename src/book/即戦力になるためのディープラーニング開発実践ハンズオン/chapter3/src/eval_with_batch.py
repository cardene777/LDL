import glob
import os

import cv2
import numpy as np
from keras.models import load_model

DATA_DIR = "data"

classes = ["person", "cat", "dog"]

model = load_model(os.path.join(
    "results", "vgg16_200epoch_lr0.01_3000images.h5"
))
input_H, input_W = model.input.shape[1:3]

images = []
labels = []

for class_index, class_name in enumerate(classes):
    files = glob.glob(os.path.join(DATA_DIR, "valid", class_name, "*.jpg"))
    for file_path in files:
        img = cv2.imread(file_path)
        img = cv2.resize(img, (input_W, input_H))
        img = img / 255
        images.append(img)
        labels.append(class_index)
images = np.array(images)

predicts = model.predict(images, batch_size=256)

predicts = predicts.argmax(axis=1)

with open(os.path.join("results", "vgg16_batch_predicts.csv"), "w") as f:
    f.write("ground_truth,predicted\n")
    for ground_truth, predicted in zip(labels, predicts):
        f.write("{},{}\n".format(ground_truth, predicted))
