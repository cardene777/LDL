import json
import os

from PIL import Image

DATASET_DIR = "path/to/coco"
OUTPUT_DIR = os.path.join("..", "data")
CATEGORIES = {
    1: "person",
    17: "cat",
    18: "dog"
}
setting_list = [
    {
        "data_num_per_class": 1000,
        "annotation_file_path": os.path.join(
            DATASET_DIR,
            "annotations",
            "instances_train2017.json"
        ),
        "src_images_dir": os.path.join(DATASET_DIR, "train2017"),
        "output_dir": os.path.join(OUTPUT_DIR, "train")
    },
    {
        "data_num_per_class": 100,
        "annotation_file_path": os.path.join(
            DATASET_DIR,
            "annotations",
            "instances_val2017.json"
        ),
        "src_images_dir": os.path.join(DATASET_DIR, "val2017"),
        "output_dir": os.path.join(OUTPUT_DIR, "valid")
    }
]

for setting in setting_list:
    print("Load annotation data : " + setting["annotation_file_path"])
    with open(setting["annotation_file_path"], "rb") as f:
        data = json.load(f)

    os.makedirs(setting["output_dir"], exist_ok=True)
    for category_name in CATEGORIES.values():
        TARGET_DIR = os.path.join(setting["output_dir"], category_name)
        os.makedirs(TARGET_DIR, exist_ok=True)

    images_info = {}
    """
    images_info = {
        "category_name": [{
            "category_id": 0,
            "bbox": [0, 100, 20, 30],  # x, y, w, h
            "area": 400
        }]
    }
    """
    for category_name in CATEGORIES.values():
        images_info[category_name] = []

    print("Filter data with each class")
    for info in data["annotations"]:
        if info["category_id"] not in CATEGORIES:
            continue
        if info["area"] < info["bbox"][2] * info["bbox"][3] * 0.5:
            continue
        category_name = CATEGORIES[info["category_id"]]
        images_info[category_name].append(info)

    for category_name in CATEGORIES.values():
        print("Crop and save images for each class : " + category_name)
        images_info[category_name].sort(key=lambda d: d["area"], reverse=True)
        images_info[category_name] = \
            images_info[category_name][:setting["data_num_per_class"]]

        for i, info in enumerate(images_info[category_name]):
            src_filename = os.path.join(
                setting["src_images_dir"],
                "{:0>12d}.jpg".format(info["image_id"])
            )
            output_filename = os.path.join(
                setting["output_dir"],
                category_name,
                "{:0>12d}.jpg".format(i)
            )
            x, y, w, h = info["bbox"]
            img = Image.open(src_filename)
            img = img.crop((x, y, x + w, y + h))
            img.save(output_filename)
