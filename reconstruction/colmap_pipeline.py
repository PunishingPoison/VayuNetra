import os
import pycolmap

def run_colmap(images_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    database_path = os.path.join(output_dir, 'database.db')
    
    # 1. Feature extraction
    print("Extracting features...")
    pycolmap.extract_features(database_path, images_dir)
    
    # 2. Feature matching
    print("Matching features...")
    pycolmap.match_exhaustive(database_path)
    
    # 3. Incremental SfM
    print("Running incremental SfM...")
    maps = pycolmap.incremental_mapping(database_path, images_dir, output_dir)
    
    if len(maps) > 0:
        print(f"Reconstruction successful. {len(maps)} maps created.")
        best_map = maps[0]
        
        # Export as text format for Nerfstudio compatibility
        sparse_dir = os.path.join(output_dir, 'sparse', '0')
        os.makedirs(sparse_dir, exist_ok=True)
        best_map.write_text(sparse_dir)
        print(f"Exported sparse model to {sparse_dir}")
    else:
        print("Reconstruction failed to find any maps.")

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    images_dir = os.path.join(base_dir, 'processed', 'frames')
    colmap_out = os.path.join(base_dir, 'colmap')
    
    run_colmap(images_dir, colmap_out)
