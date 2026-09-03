import os
import subprocess
import sys

def main():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    print("========================================")
    print(" STEP 1: CONVERTING TELEMETRY (BYPASSING COLMAP) ")
    print("========================================")
    convert_script = os.path.join(base_dir, 'scripts', 'convert_telemetry.py')
    result = subprocess.run(["python", convert_script])
    
    if result.returncode != 0:
        print("Error: Telemetry conversion failed! Aborting training.")
        sys.exit(1)
    
    print("========================================")
    print(" STEP 2: FAST LOCAL GAUSSIAN SPLATTING ")
    print("========================================")
    ns_data_dir = os.path.join(base_dir, 'data', 'nerfstudio')
    output_dir = os.path.join(base_dir, 'outputs', 'local_splats')
    
    cmd = [
        "ns-train",
        "splatfacto",
        "--data", ns_data_dir,
        "--output-dir", output_dir,
        "--viewer.websocket-port", "7007",
        "--pipeline.model.camera-optimizer.mode", "off",
        "--pipeline.model.random-scale", "0.2",
        "--max-num-iterations", "15000"
    ]
    
    print(f"Executing: {' '.join(cmd)}")
    subprocess.run(cmd)

if __name__ == "__main__":
    main()
