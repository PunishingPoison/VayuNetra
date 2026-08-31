import os
import csv
import json

def ingest_telemetry(raw_dir, output_manifest):
    telemetry_csv = os.path.join(raw_dir, 'telemetry.csv')
    
    if not os.path.exists(telemetry_csv):
        print(f"Error: {telemetry_csv} not found.")
        return
        
    manifest = {
        "frames": []
    }
    
    with open(telemetry_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            frame_data = {
                "image_name": row["image_name"],
                "timestamp": float(row["timestamp"]),
                "gps": {
                    "lat": float(row["lat"]),
                    "lon": float(row["lon"]),
                    "alt": float(row["alt"])
                },
                "orientation": {
                    "w": float(row["qw"]),
                    "x": float(row["qx"]),
                    "y": float(row["qy"]),
                    "z": float(row["qz"])
                }
            }
            manifest["frames"].append(frame_data)
            
    with open(output_manifest, 'w') as f:
        json.dump(manifest, f, indent=4)
        
    print(f"Ingested {len(manifest['frames'])} frames into {output_manifest}")

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    raw_dir = os.path.join(base_dir, 'raw')
    manifest_path = os.path.join(base_dir, 'manifests', 'capture_manifest.json')
    
    ingest_telemetry(raw_dir, manifest_path)
