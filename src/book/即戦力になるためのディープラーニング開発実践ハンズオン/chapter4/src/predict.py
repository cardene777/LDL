import os

import cv2
from keras.models import load_model
from utils import ImageLoader


MODEL_FILE_NAME = 'autoencoder_experiment_01.h5'
MODEL_PATH = os.path.join('results', MODEL_FILE_NAME)
DATA_DIR = os.path.join('data')
TRAIN_DATA_DIR = os.path.join(DATA_DIR, 'train')
VALID_DATA_DIR = os.path.join(DATA_DIR, 'valid')
EVAL_OK_DATA_DIR = os.path.join(DATA_DIR, 'eval_ok')
EVAL_NG_DATA_DIR = os.path.join(DATA_DIR, 'eval_ng')
OUTPUT_DIR = os.path.join('outputs')
TRAIN_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'train')
VALID_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'valid')
EVAL_OK_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'eval_ok')
EVAL_NG_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'eval_ng')


model = load_model(MODEL_PATH)
image_size = model.input.shape[1:3]
image_size = tuple(image_size)

def predicts(images, filenames, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    print('predicts ', len(images), ' files .')
    preds = model.predict(images)
    for img, fname, pred in zip(images, filenames, preds):
        output_img = pred * 255

        output_path = os.path.join(output_dir, os.path.basename(fname))
        cv2.imwrite(output_path, output_img)
    print('saved predicts .')

train_images, train_fnames = ImageLoader(TRAIN_DATA_DIR, image_size).load(with_filenames=True)
valid_images, valid_fnames = ImageLoader(VALID_DATA_DIR, image_size).load(with_filenames=True)
eval_ok_images, eval_ok_fnames = ImageLoader(EVAL_OK_DATA_DIR, image_size).load(with_filenames=True)
eval_ng_images, eval_ng_fnames = ImageLoader(EVAL_NG_DATA_DIR, image_size).load(with_filenames=True)

predicts(train_images, train_fnames, TRAIN_OUTPUT_DIR)
predicts(valid_images, valid_fnames, VALID_OUTPUT_DIR)
predicts(eval_ok_images, eval_ok_fnames, EVAL_OK_OUTPUT_DIR)
predicts(eval_ng_images, eval_ng_fnames, EVAL_NG_OUTPUT_DIR)
