import cv2
import glob
import numpy as np
import os


class ImageLoader():
    def __init__(self, dir_path, image_size, binary_th=120):
        self.__dir_path = dir_path
        self.__image_size = image_size
        self.__binary_th = binary_th


    def load(self):
        images = []
        files = glob.glob(os.path.join(self.__dir_path, '*.png'))
        files.sort()
        for file_path in files:
            img = cv2.imread(file_path)
            img = cv2.resize(img, self.__image_size)

            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img[img <= self.__binary_th] = 0
            img[img > self.__binary_th] = 1
            img = np.expand_dims(img, axis=2)
            img = img / 255

            images.append(img)
        images = np.array(images)
        return images
