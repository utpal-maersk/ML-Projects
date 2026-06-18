import os
import shutil
import random

SOURCE_DIR = "/Users/utpal.gohain/Documents/Ml-project/plant_disease_project/dataset/train"
TEST_DIR = "/Users/utpal.gohain/Documents/Ml-project/plant_disease_project/dataset/test"

SPLIT_PERCENT = 0.20  # 20%

classes = os.listdir(SOURCE_DIR)

for class_name in classes:

    source_class = os.path.join(
        SOURCE_DIR,
        class_name
    )

    test_class = os.path.join(
        TEST_DIR,
        class_name
    )

    os.makedirs(
        test_class,
        exist_ok=True
    )

    images = os.listdir(
        source_class
    )

    random.shuffle(
        images
    )

    num_test = int(
        len(images) * SPLIT_PERCENT
    )

    test_images = images[:num_test]

    for img in test_images:

        src = os.path.join(
            source_class,
            img
        )

        dst = os.path.join(
            test_class,
            img
        )

        shutil.move(
            src,
            dst
        )

print("✅ Dataset split complete")