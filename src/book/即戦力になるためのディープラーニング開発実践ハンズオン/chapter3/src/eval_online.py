import os
import glob

import cv2
import numpy as np
from keras.models import load_model

DATA_DIR = "data"

classes = ["person", "cat", "dog"]

model = load_model(os.path.join(
    "results", "vgg16_10epoch_lr0.01_30images_online.h5"
))
input_H, input_W = model.input.shape[1:3]

csv_writer = open(os.path.join(
    "results", "vgg16_online_predicts.csv"
), "w")
csv_writer.write("ground_truth,predicted\n")

for class_index, class_name in enumerate(classes):
    files = glob.glob(os.path.join(DATA_DIR, "valid", class_name, "*.jpg"))
    for file_path in files:
        img = cv2.imread(file_path)
        img = cv2.resize(img, (input_W, input_H))
        img = img / 255
        img = np.array([img])
        predict = model.predict(img)
        csv_writer.write("{},{}\n".format(class_index, predict[0].argmax()))

csv_writer.close()
