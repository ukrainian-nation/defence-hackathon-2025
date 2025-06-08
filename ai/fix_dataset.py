import os
from PIL import Image

# Destination directories
train_labels_dest = './datasets/drone-detection-new.v5-new-train.yolov8/train/labels'
valid_labels_dest = './datasets/drone-detection-new.v5-new-train.yolov8/valid/labels'
test_labels_dest = './datasets/drone-detection-new.v5-new-train.yolov8/test/labels'

# Move .jpg files to images directories
train_images_dest = './datasets/drone-detection-new.v5-new-train.yolov8/train/images'
valid_images_dest = './datasets/drone-detection-new.v5-new-train.yolov8/valid/images'
test_images_dest = './datasets/drone-detection-new.v5-new-train.yolov8/test/images'

def resize_image_and_update_labels(image_path, label_path, output_image_path, output_label_path, new_size=(640, 640)):
    # Resize image
    try:
        with Image.open(image_path) as img:
            original_size = img.size
            img_resized = img.resize(new_size)
            img_resized.save(output_image_path)
    except Exception as e:
        print(f"Deleting invalid image file: {image_path} due to error: {e}")
        os.remove(image_path)
        return

    # Update label file
    with open(label_path, 'r') as label_file:
        lines = label_file.readlines()

    updated_lines = []
    for line in lines:
        parts = line.strip().split()
        class_id = parts[0]
        x_center, y_center, width, height = map(float, parts[1:])
        
        # Adjust coordinates based on new size
        x_center = x_center * new_size[0] / original_size[0]
        y_center = y_center * new_size[1] / original_size[1]
        width = width * new_size[0] / original_size[0]
        height = height * new_size[1] / original_size[1]
        
        updated_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

    with open(output_label_path, 'w') as output_label_file:
        output_label_file.writelines(updated_lines)

# Directory paths
test_images_dir = './datasets/drone-detection-new.v5-new-train.yolov8/train/images'
test_labels_dir = './datasets/drone-detection-new.v5-new-train.yolov8/train/labels'

# Iterate through test images and resize them
for filename in os.listdir(test_images_dir):
    if filename.endswith('.jpg'):
        image_path = os.path.join(test_images_dir, filename)
        label_path = os.path.join(test_labels_dir, filename.replace('.jpg', '.txt'))
        
        output_image_path = os.path.join(test_images_dir, filename)  # Overwrite original image
        output_label_path = os.path.join(test_labels_dir, filename.replace('.jpg', '.txt'))  # Overwrite original label
        
        if os.path.exists(label_path):  # Ensure corresponding label file exists
            resize_image_and_update_labels(image_path, label_path, output_image_path, output_label_path)