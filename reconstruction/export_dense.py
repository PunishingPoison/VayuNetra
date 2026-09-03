import os
import subprocess
import glob
import numpy as np
from plyfile import PlyData

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    output_dir = os.path.join(base_dir, 'outputs', 'splats')
    
    print("Finding the latest AI model...")
    search_path = os.path.join(output_dir, 'unnamed', 'splatfacto', '*', 'config.yml')
    configs = glob.glob(search_path)
    if not configs:
        print("Could not find config.yml!")
        exit(1)
        
    latest_config = max(configs, key=os.path.getctime)
    export_dir = os.path.join(output_dir, 'export_dense')
    os.makedirs(export_dir, exist_ok=True)
    
    print("Commanding AI to generate a DENSE Point Cloud (1 Million Points)...")
    # Using open3d normals since splatfacto doesn't predict normals natively
    export_cmd = [
        "ns-export",
        "pointcloud",
        "--load-config", latest_config,
        "--output-dir", export_dir,
        "--num-points", "1000000",
        "--remove-outliers", "True",
        "--normal-method", "open3d"
    ]
    subprocess.run(export_cmd)
    
    print("Converting dense .ply to Unreal Engine .txt format...")
    ply_path = os.path.join(export_dir, 'point_cloud.ply')
    txt_path = os.path.join(export_dir, 'dense_road.txt')
    
    if not os.path.exists(ply_path):
        print("Failed to find point_cloud.ply")
        return
        
    plydata = PlyData.read(ply_path)
    vertex = plydata['vertex']
    
    x = vertex['x']
    y = vertex['y']
    z = vertex['z']
    r = vertex['red']
    g = vertex['green']
    b = vertex['blue']
    
    print("Writing 1,000,000 points to text file...")
    with open(txt_path, 'w') as f:
        for i in range(len(x)):
            f.write(f"{x[i]} {y[i]} {z[i]} {r[i]} {g[i]} {b[i]}\n")
            
    print(f"SUCCESS! Dense point cloud ready at: {txt_path}")

if __name__ == "__main__":
    main()
