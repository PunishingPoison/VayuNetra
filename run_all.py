import os
import subprocess

def main():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    print("========================================")
    print(" STEP 1: CAPTURING DRONE DATA (ROAD)")
    print("========================================")
    subprocess.run(["python", r"scripts\capture_synthetic.py"])
    
    print("========================================")
    print(" STEP 2: PROCESSING (INGEST, SELECT, COLMAP)")
    print("========================================")
    subprocess.run(["python", r"reconstruction\ingest.py"])
    subprocess.run(["python", r"reconstruction\frame_selection.py"])
    subprocess.run(["python", r"reconstruction\colmap_pipeline.py"])
    
    print("========================================")
    print(" STEP 3: TRAINING AI & EXPORTING")
    print("========================================")
    subprocess.run(["python", r"reconstruction\train_splat.py"])
    
    print("========================================")
    print(" DONE! IMPORT SPLAT.TXT INTO UNREAL")
    print("========================================")

if __name__ == "__main__":
    main()
