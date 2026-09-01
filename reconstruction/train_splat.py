import os
import subprocess

def train_splat(data_dir, output_dir):
    print("Starting Splatfacto training via Nerfstudio...")
    
    # Normally we run: ns-train splatfacto --data <colmap_dir>
    # We will output to our outputs/splats dir
    
    cmd = [
        "ns-train",
        "splatfacto",
        "--output-dir", output_dir,
        "--viewer.websocket-port", "7007",
        "colmap",
        "--data", data_dir,
        "--colmap-path", os.path.join(base_dir, 'data', 'colmap', 'sparse', '0')
    ]
    
    # This spawns the training process. 
    # In a real environment, this blocks until training is stopped or reaches max iterations.
    print(f"Executing: {' '.join(cmd)}")
    subprocess.run(cmd)

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # Give Nerfstudio the base data folder, and explicitly tell it where images and colmap are
    data_dir = os.path.join(base_dir, 'data')
    images_dir = os.path.join(base_dir, 'data', 'processed', 'frames')
    colmap_dir = os.path.join(base_dir, 'data', 'colmap', 'sparse', '0')
    output_dir = os.path.join(base_dir, 'outputs', 'splats')
    
    cmd = [
        "ns-train",
        "splatfacto",
        "--output-dir", output_dir,
        "--viewer.websocket-port", "7007",
        "colmap",
        "--data", data_dir,
        "--images-path", images_dir,
        "--colmap-path", colmap_dir
    ]
    
    print(f"Executing: {' '.join(cmd)}")
    subprocess.run(cmd)
