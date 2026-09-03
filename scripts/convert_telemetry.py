import os
import json
import numpy as np
import csv
from scipy.spatial.transform import Rotation as R
import math
import shutil

def build_nerfstudio_transforms(telemetry_csv_path, raw_dir, output_dir, image_width=256, image_height=144, fov_degrees=90.0):
    images_dir = os.path.join(output_dir, 'images')
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
        
    output_json_path = os.path.join(output_dir, 'transforms.json')
    
    fov_rad = math.radians(fov_degrees)
    focal_length = (image_width / 2.0) / math.tan(fov_rad / 2.0)
    cx = image_width / 2.0
    cy = image_height / 2.0

    M_ue_to_ns_world = np.array([
        [0, 1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ], dtype=float)

    R_gl_to_ue_cam = np.array([
        [ 0,  0, -1],
        [ 1,  0,  0],
        [ 0,  1,  0]
    ], dtype=float)

    frames = []

    with open(telemetry_csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            image_filename = row['image_name']
            src_filepath = os.path.join(raw_dir, image_filename)
            dest_filepath = os.path.join(images_dir, image_filename)
            
            if not os.path.exists(src_filepath):
                print(f"Skipping {image_filename}, file not found.")
                continue
                
            shutil.copy2(src_filepath, dest_filepath)

            t_ue = np.array([float(row['lat']), float(row['lon']), float(row['alt'])])
            quat = [float(row['qx']), float(row['qy']), float(row['qz']), float(row['qw'])]
            r_drone = R.from_quat(quat)
            R_ue = r_drone.as_matrix()

            R_c2w = M_ue_to_ns_world @ R_ue @ R_gl_to_ue_cam
            t_ns = M_ue_to_ns_world @ t_ue

            c2w_matrix = np.eye(4)
            c2w_matrix[:3, :3] = R_c2w
            c2w_matrix[:3, 3] = t_ns

            frames.append({
                "file_path": f"images/{image_filename}",
                "transform_matrix": c2w_matrix.tolist()
            })

    transforms_dict = {
        "camera_model": "OPENCV",
        "fl_x": focal_length,
        "fl_y": focal_length,
        "cx": cx,
        "cy": cy,
        "w": image_width,
        "h": image_height,
        "k1": 0.0,
        "k2": 0.0,
        "p1": 0.0,
        "p2": 0.0,
        "frames": frames
    }

    with open(output_json_path, 'w') as f:
        json.dump(transforms_dict, f, indent=4)
    print(f"Success: Processed {len(frames)} frames into {output_json_path}")

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    raw_dir = os.path.join(base_dir, 'data', 'raw')
    telemetry_path = os.path.join(raw_dir, 'telemetry.csv')
    output_dir = os.path.join(base_dir, 'data', 'nerfstudio')
    
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    build_nerfstudio_transforms(telemetry_path, raw_dir, output_dir)
