import os
import numpy as np
import cv2
from tqdm import tqdm

# Set the path to the Luna16 dataset
data_dir = 'data/luna16/images/subset0/'

# Define the classes for the YOLO model
classes = ['nodule']

# Define the size of the input image for YOLO
img_size = (416, 416)

# Define the denoising parameters
kernel_size = (5, 5)
sigmaX = 10

# Define a function to convert the Luna16 annotations to YOLO format
def convert_annotation(img_size, anno):
    x_min, y_min, x_max, y_max = anno[:4]
    width, height = img_size
    x_center = (x_min + x_max) / 2 / width
    y_center = (y_min + y_max) / 2 / height
    w = (x_max - x_min) / width
    h = (y_max - y_min) / height
    class_id = classes.index(anno[4])
    return (class_id, x_center, y_center, w, h)

# Load the Luna16 dataset
with open(os.path.join('data/luna16/csv/candidates_V2.csv')) as f:
    annotations = f.readlines()

# Create the output directory for the preprocessed data
outputDir = 'data/luna16/marked_images/'
os.makedirs(outputDir, exist_ok=True)

# Iterate over the .mhd files in the data_dir directory and preprocess the corresponding CT scan images
for filename in tqdm([f for f in os.listdir(data_dir) if f.endswith('.mhd')]):
    path = os.path.join(data_dir, filename)
    print(f"Loading image: {path}")
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    
    """
    # Apply denoising
    img = cv2.GaussianBlur(img, kernel_size, sigmaX)

    # Resize the image to the input size of the YOLO model
    img = cv2.resize(img, img_size)
    """
    # Draw bounding boxes on the image
    for line in annotations:
        parts = line.strip().split(',')
        if parts[0] == filename[:-4]:
            annos = parts[1:]
            for anno in annos:
                anno = anno.split()
                if anno[4] == 'nodule':
                    x_min, y_min, x_max, y_max = [int(float(a)) for a in anno[:4]]
                    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)
    
    # Save the preprocessed image
    cv2.imwrite(os.path.join(outputDir, filename[:-4] + '.jpg'), img)
