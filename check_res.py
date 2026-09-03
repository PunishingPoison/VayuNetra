import cv2
import glob
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'raw'))
files = glob.glob(os.path.join(base_dir, '*.png'))
if files:
    img = cv2.imread(files[0])
    print(f"Image shape: {img.shape}")
else:
    print("No images found.")
