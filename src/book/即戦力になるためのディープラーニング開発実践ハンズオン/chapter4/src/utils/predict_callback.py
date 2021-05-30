import os
import cv2
import math
import numpy as np
import keras.callbacks as KC


class PredictCallback(KC.Callback):
    """
    Predict Callback Class
    """

    def __init__(self, targets, output_dir, block_size=3, period=1, verbose=0):
        super(PredictCallback, self).__init__()
        self.__targets = targets
        self.__output_dir = output_dir
        self.__verbose = verbose
        self.__period = period
        self.__block_size = block_size


    def __log(self, *args):
        if self.__verbose > 0:
            print('<PredictCallback> ', *args)


    def on_epoch_end(self, epoch, logs=None):
        if (epoch + 1) % self.__period != 0:
            return

        if len(self.__targets) < 1:
            return

        preds = self.model.predict(self.__targets)
        preds = preds * 255

        preds_img = self.__make_image_tile(preds)

        filename = 'Epoch%04d_predict.png' % (epoch + 1)
        save_path = os.path.join(self.__output_dir, filename)
        cv2.imwrite(save_path, preds_img)

        self.__log('\nEpoch %04d: saving preds .' % (epoch + 1))


    def __make_image_tile(self, imgs):
        split_num = math.ceil(len(imgs) / self.__block_size)
        img_block_hs = np.array_split(imgs, split_num)
        img_block = []
        for img_block_h in img_block_hs:
            img_block_ws = []
            for img_block_w in img_block_h:
                img_block_ws.append(img_block_w)
            img_block.append(np.hstack(img_block_ws))
        return np.vstack(img_block)
