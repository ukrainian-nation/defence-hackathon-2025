import cv2
from ultralytics import YOLO  # assuming you are using YOLOv5 or YOLOv8 (depending on your model)
import numpy as np

model = YOLO("../runs/detect/train/weights/best.pt")

image_paths = ["testdata/V_AIRPLANE_0033_065_png.rf.61a2f3f3257c0c1a51e2d1bcc6bec1a3.jpg", "testdata/V_BIRD_02180_100_png.rf.9cf9189308cf796bcbc7bf14b8beeafc.jpg", "testdata/V_HELICOPTER_011235_151_png.rf.9931cf3078ad9f0fcd3c960c0a1cf794.jpg"]

for image_path in image_paths:
    print(image_path)
    # Read the input image
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Unable to read image {image_path}")
        continue

    # Make predictions on the image
    results = model(image)

    # Render predictions on the image (bounding boxes, labels, etc.)
    annotated_image = results[0].plot()

    # Display the result
    cv2.imshow(f"Annotated Image: {image_path}", annotated_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        continue


# Clean up
cv2.destroyAllWindows()
