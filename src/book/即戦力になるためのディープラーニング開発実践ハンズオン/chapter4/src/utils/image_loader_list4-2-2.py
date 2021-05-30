import cv2
import glob
import numpy as np
import os


class ImageLoader():
    def __init__(self, dir_path, image_size):
        self.__dir_path = dir_path
        self.__image_size = image_size

    def load(self, with_filenames=False):
        images = []
        files = glob.glob(os.path.join(self.__dir_path, '*.png'))
        files.sort()
        for file_path in files:
            img = cv2.imread(file_path)
            img = cv2.resize(img, self.__image_size)
            img = img / 255
            images.append(img)
        images = np.array(images)
        if with_filenames:
            return images, files
        return images
