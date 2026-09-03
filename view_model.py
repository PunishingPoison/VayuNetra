import os
import glob
import subprocess

def main():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    output_dir = os.path.join(base_dir, 'outputs', 'splats')
    
    # Search for the latest splatfacto config
    search_path = os.path.join(output_dir, 'unnamed', 'splatfacto', '*', 'config.yml')
    configs = glob.glob(search_path)
    
    if not configs:
        print("Could not find a trained model!")
        exit(1)
        
    latest_config = max(configs, key=os.path.getctime)
    print("========================================")
    print(" LAUNCHING DEDICATED 3D VIEWER ")
    print("========================================")
    print(f"Loading model: {latest_config}")
    
    cmd = [
        "ns-viewer",
        "--load-config", latest_config,
        "--viewer.websocket-port", "7007"
    ]
    
    subprocess.run(cmd)

if __name__ == "__main__":
    main()
