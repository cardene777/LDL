import cv2
import glob
import os

from keras.callbacks import TensorBoard

from models import AutoEncoder
from utils import ImageLoader


DATA_DIR = os.path.join('data')
TRAIN_DATA_DIR = os.path.join(DATA_DIR, 'train')
VALID_DATA_DIR = os.path.join(DATA_DIR, 'valid')
LOGS_DIR = os.path.join('logs')
MODEL_FILEPATH = os.path.join('results', 'autoencoder_experiment_01.h5')


model = AutoEncoder(gpu_num=8)
image_size = model.input.shape[1:3]

model.summary()

train_images = ImageLoader(TRAIN_DATA_DIR, tuple(image_size)).load()
valid_images = ImageLoader(VALID_DATA_DIR, tuple(image_size)).load()

tensorboard_callback = TensorBoard(log_dir=LOGS_DIR)

model.fit(
    train_images,
    train_images,
    validation_data=(valid_images, valid_images),
    batch_size=125,
    epochs=100,
    callbacks=[tensorboard_callback]
)

model.save(MODEL_FILEPATH)
