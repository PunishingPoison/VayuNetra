import os
import subprocess

def train_splat(data_dir, output_dir):
    print("Starting Splatfacto training via Nerfstudio...")
    
    # Normally we run: ns-train splatfacto --data <colmap_dir>
    # We will output to our outputs/splats dir
    
    cmd = [
        "ns-train",
        "splatfacto",
        "--data", data_dir,
        "--output-dir", output_dir,
        "--pipeline.model.cull_alpha_thresh", "0.005",
        "--pipeline.model.continue_cull_post_densification", "False",
        "--viewer.websocket-port", "7007"
    ]
    
    # This spawns the training process. 
    # In a real environment, this blocks until training is stopped or reaches max iterations.
    print(f"Executing: {' '.join(cmd)}")
    subprocess.run(cmd)

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(base_dir, 'data', 'processed', 'frames') # Nerfstudio parses COLMAP out of here
    # Assuming colmap data is actually in data/colmap or data/processed/frames/colmap
    # Standard Nerfstudio expects a 'colmap' folder inside the data_dir, so we should ensure 
    # our colmap pipeline writes to data_dir/colmap/sparse/0
    
    output_dir = os.path.join(base_dir, 'outputs', 'splats')
    
    train_splat(data_dir, output_dir)
