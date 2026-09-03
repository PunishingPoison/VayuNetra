import os
import glob
import subprocess

def main():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    output_dir = os.path.join(base_dir, 'outputs', 'local_splats')
    
    print("========================================")
    print(" STEP 3: EXPORTING .PLY FOR UNREAL ENGINE ")
    print("========================================")
    
    # Search for the latest splatfacto config
    search_path = os.path.join(output_dir, 'nerfstudio', 'splatfacto', '*', 'config.yml')
    configs = glob.glob(search_path)
    
    if not configs:
        print("Error: Could not find a trained model config.yml!")
        exit(1)
        
    latest_config = max(configs, key=os.path.getctime)
    export_dir = os.path.join(base_dir, 'outputs', 'final_model')
    
    cmd = [
        "ns-export",
        "gaussian-splat",
        "--load-config", latest_config,
        "--output-dir", export_dir
    ]
    
    print(f"Exporting model from config: {latest_config}")
    subprocess.run(cmd)
    
    print("========================================")
    print(" SUCCESS! ")
    print(f" Your final 3D model is ready at: {os.path.join(export_dir, 'splat.ply')}")
    print("========================================")

if __name__ == "__main__":
    main()
