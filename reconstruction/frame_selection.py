import os
import cv2
import json
import shutil

def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

def select_frames(manifest_path, raw_dir, processed_dir, blur_threshold=100.0, max_frames=200):
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
        
    os.makedirs(processed_dir, exist_ok=True)
    
    selected_frames = []
    
    # Optional: downsample based on total frame count to avoid bloat
    step = max(1, len(manifest["frames"]) // max_frames)
    
    print(f"Total raw frames: {len(manifest['frames'])}")
    
    for i, frame in enumerate(manifest["frames"]):
        if i % step != 0:
            continue
            
        img_name = frame["image_name"]
        img_path = os.path.join(raw_dir, img_name)
        
        if not os.path.exists(img_path):
            continue
            
        image = cv2.imread(img_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fm = variance_of_laplacian(gray)
        
        if fm > blur_threshold:
            # Frame is sharp enough
            dest_path = os.path.join(processed_dir, img_name)
            shutil.copy2(img_path, dest_path)
            frame["blur_score"] = fm
            selected_frames.append(frame)
        else:
            print(f"Skipping {img_name} due to blur (score: {fm:.2f})")
            
    # Update manifest with selected frames
    processed_manifest = os.path.join(os.path.dirname(manifest_path), 'processed_manifest.json')
    with open(processed_manifest, 'w') as f:
        json.dump({"frames": selected_frames}, f, indent=4)
        
    print(f"Selected {len(selected_frames)} sharp frames. Saved to {processed_dir}")

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    raw_dir = os.path.join(base_dir, 'raw')
    processed_dir = os.path.join(base_dir, 'processed', 'frames')
    manifest_path = os.path.join(base_dir, 'manifests', 'capture_manifest.json')
    
    select_frames(manifest_path, raw_dir, processed_dir)
