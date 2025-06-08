import os
from PIL import Image

# Destination directories
labels_dirs = [
    './datasets/drone-detection-new.v5-new-train.yolov8/train/labels',
    './datasets/drone-detection-new.v5-new-train.yolov8/valid/labels',
    './datasets/drone-detection-new.v5-new-train.yolov8/test/labels'
]

# Move .jpg files to images directories
images_dirs = [
    './datasets/drone-detection-new.v5-new-train.yolov8/train/images',
    './datasets/drone-detection-new.v5-new-train.yolov8/valid/images',
    './datasets/drone-detection-new.v5-new-train.yolov8/test/images'
]

prefixes = ['V_DRONE_', 'V_AIRPLANE_']


def process_labels(labels_dirs, prefixes):
    for dir_path in labels_dirs:
        for file_name in os.listdir(dir_path):
            if any(file_name.startswith(prefix) for prefix in prefixes):
                file_path = os.path.join(dir_path, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                except UnicodeDecodeError:
                    print(f"Skipping file due to encoding error: {file_path}")
                    continue

                if not lines:  # Skip empty files
                    continue

                updated_lines = []
                for line in lines:
                    parts = line.split()
                    if parts:
                        if parts[0] == '0':
                            parts[0] = '1'
                        elif parts[0] == '1':
                            parts[0] = '0'
                        updated_lines.append(' '.join(parts))

                if updated_lines:  # If there are updated lines, overwrite the file
                    with open(file_path, 'w') as file:
                        file.write('\n'.join(updated_lines))
                else:  # If all lines were removed, skip deleting the file
                    continue

process_labels(labels_dirs, prefixes)
