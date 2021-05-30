def cut_centers(target_dir, cut_dir):
    os.makedirs(cut_dir, exist_ok=True)

    files = glob.glob(os.path.join(target_dir, '*.png'))
    files.sort()

    for fpath in files:
        img = cv2.imread(fpath)
        img_h, img_w = np.shape(img)[:2]

        half_h = img_h // 2
        half_w = img_w // 2
        half_half_h = half_h // 2
        half_half_w = half_w // 2
        cut_img = img[half_h-half_half_h:half_h+half_half_h
                    , half_w-half_half_w:half_w+half_half_w]

        fname = os.path.basename(fpath)
        save_path = os.path.join(save_dir, fname)
        cv2.imwrite(save_path, cut_img)

TRAIN = 'train'
VALID = 'valid'
EVAL_OK = 'eval_ok'
EVAL_NG = 'eval_ng'

def DATA_DIR(data_type):
    return os.path.join('.', 'data', data_type)

def CUT_DIR(data_type):
    return os.path.join('.', 'cut_data', data_type)

cut_centers(DATA_DIR(TRAIN), CUT_DIR(TRAIN))
cut_centers(DATA_DIR(VALID), CUT_DIR(VALID))
cut_centers(DATA_DIR(EVAL_OK), CUT_DIR(EVAL_OK))
cut_centers(DATA_DIR(EVAL_NG), CUT_DIR(EVAL_NG))
