def isolate_dark_data(target_dir, bright_dir, dark_dir, th=0.25):
    os.makedirs(bright_dir, exist_ok=True)
    os.makedirs(dark_dir, exist_ok=True)

    files = glob.glob(os.path.join(target_dir, '*.png'))
    files.sort()

    for fpath in files:
        img_org = cv2.imread(fpath)
        img = cv2.imread(fpath)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img[img <= COL_TH] = 0
        img[img > COL_TH] = 1

        bright_value = np.average(img)

        fname = os.path.basename(fpath)
        save_path = os.path.join(bright_dir, fname)
        if bright_value < th:
            save_path = os.path.join(dark_dir, fname)
        cv2.imwrite(save_path, img_org)

def BRIGHT_DIR(data_type):
    return os.path.join('.', 'isolate_data', 'bright', data_type)

def DARK_DIR(data_type):
    return os.path.join('.', 'isolate_data', 'dark', data_type)

isolate_dark_data(CUT_DIR(TRAIN), BRIGHT_DIR(TRAIN), DARK_DIR(TRAIN))
isolate_dark_data(CUT_DIR(VALID), BRIGHT_DIR(TRAIN), DARK_DIR(VALID))
isolate_dark_data(CUT_DIR(EVAL_OK), BRIGHT_DIR(EVAL_OK), DARK_DIR(EVAL_OK))
isolate_dark_data(CUT_DIR(EVAL_NG), BRIGHT_DIR(EVAL_NG), DARK_DIR(EVAL_NG), th=0.1)
