import os
import subprocess
import glob

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    data_dir = os.path.join(base_dir, 'data')
    images_dir = os.path.join(base_dir, 'data', 'processed', 'frames')
    colmap_dir = os.path.join(base_dir, 'data', 'colmap', 'sparse', '0')
    output_dir = os.path.join(base_dir, 'outputs', 'meshes')
    
    print("========================================")
    print(" STEP 1: FAST TRAINING NeRF (2000 Steps)")
    print("========================================")
    train_cmd = [
        "ns-train",
        "nerfacto",
        "--pipeline.model.predict-normals", "True",
        "--max-num-iterations", "2000",
        "--output-dir", output_dir,
        "--viewer.websocket-port", "7007",
        "colmap",
        "--data", data_dir,
        "--images-path", images_dir,
        "--colmap-path", colmap_dir
    ]
    subprocess.run(train_cmd)
    
    print("========================================")
    print(" STEP 2: EXPORTING SOLID 3D MESH (.OBJ) ")
    print("========================================")
    search_path = os.path.join(output_dir, 'unnamed', 'nerfacto', '*', 'config.yml')
    configs = glob.glob(search_path)
    if not configs:
        print("Could not find config.yml!")
        exit(1)
        
    latest_config = max(configs, key=os.path.getctime)
    export_dir = os.path.join(output_dir, 'export_obj')
    
    export_cmd = [
        "ns-export",
        "poisson",
        "--load-config", latest_config,
        "--output-dir", export_dir,
        "--target-num-faces", "500000"
    ]
    subprocess.run(export_cmd)
    
    print("========================================")
    print(" SUCCESS! ")
    print(f" Your solid 3D mesh is ready at: {export_dir}")
    print(" Drag the .obj file directly into Unreal Engine!")
    print("========================================")

if __name__ == "__main__":
    main()
