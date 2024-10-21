import json
import os

from PIL import Image

DATA_PATH = "crowdhuman"
OUT_PATH = DATA_PATH + "/annotations"
SPLITS = ["val", "train"]


def convert(odgt_file, json_file):
    # create output dir
    os.makedirs(OUT_PATH, exist_ok=True)

    data = []
    with open(odgt_file, "r") as f:
        for line in f:
            data.append(json.loads(line))

    annotations = []
    images = []
    obj_count = 0
    for i, item in enumerate(data):
        file_name = item["ID"] + ".jpg"
        image = Image.open(os.path.join(DATA_PATH, "Images", file_name))
        w, h = image.size
        image = {"file_name": file_name, "height": h, "width": w, "id": i}
        images.append(image)

        for j, gt in enumerate(item["gtboxes"]):
            if "extra" in gt:
                if "ignore" in gt["extra"]:
                    if gt["extra"]["ignore"] != 0:
                        continue
            bbox = gt["fbox"]
            ann = {
                "area": bbox[2] * bbox[3],
                "iscrowd": 0,
                "image_id": i,
                "bbox": bbox,
                "category_id": 1,
                "id": obj_count,
                "ignore": 0,
                "segmentation": [],
            }
            obj_count += 1
            annotations.append(ann)

    coco_format_json = {
        "images": images,
        "annotations": annotations,
        "categories": [{"id": 1, "name": "person"}],
    }

    with open(json_file, "w") as f:
        json.dump(coco_format_json, f)


# 変換の実行
for split in SPLITS:
    convert(f"{DATA_PATH}/annotation_{split}.odgt", f"{OUT_PATH}/{split}.json")
