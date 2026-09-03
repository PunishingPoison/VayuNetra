import os
import subprocess
import glob

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
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

    # AUTO EXPORT
    print("Training complete! Auto-exporting splat...")
    search_path = os.path.join(output_dir, 'unnamed', 'splatfacto', '*', 'config.yml')
    configs = glob.glob(search_path)
    if not configs:
        print("Could not find config.yml to export!")
        exit(1)
        
    latest_config = max(configs, key=os.path.getctime)
    export_dir = os.path.join(output_dir, 'export')
    
    export_cmd = [
        "ns-export",
        "gaussian-splat",
        "--load-config", latest_config,
        "--output-dir", export_dir
    ]
    subprocess.run(export_cmd)
    
    # AUTO CONVERT
    print("Auto-converting to TXT for Unreal Engine...")
    convert_script = os.path.join(export_dir, 'convert.py')
    subprocess.run(["python", convert_script])
    print("ALL DONE! The new splat.txt is ready for Unreal Engine!")

