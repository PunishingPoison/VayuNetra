import airsim
import time
import os
import math
import csv
import shutil

def clear_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    raw_dir = os.path.join(base_dir, 'raw')
    processed_dir = os.path.join(base_dir, 'processed', 'frames')
    colmap_dir = os.path.join(base_dir, 'colmap')
    manifest_dir = os.path.join(base_dir, 'manifests')
    
    clear_dir(raw_dir)
    clear_dir(processed_dir)
    clear_dir(colmap_dir)
    clear_dir(manifest_dir)
    
    print("Connecting to AirSim...")
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)
    
    print("Taking off...")
    client.takeoffAsync().join()
    
    # Tilt camera down 35 degrees for photogrammetry
    print("Tilting camera down for 3D scanning...")
    pitch = -math.radians(35)
    client.simSetCameraPose("0", airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(pitch, 0, 0)))
    time.sleep(1)
    
    csv_file = open(os.path.join(raw_dir, 'telemetry.csv'), 'w', newline='')
    writer = csv.writer(csv_file)
    writer.writerow(['image_name', 'timestamp', 'lat', 'lon', 'alt', 'qw', 'qx', 'qy', 'qz'])
    
    def capture_frame(idx):
        responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene)])
        if responses:
            res = responses[0]
            filename = f"frame_{idx:03d}.png"
            filepath = os.path.join(raw_dir, filename)
            airsim.write_file(filepath, res.image_data_uint8)
            
            gps = client.getMultirotorState().kinematics_estimated.position
            ori = client.getMultirotorState().kinematics_estimated.orientation
            writer.writerow([filename, time.time(), gps.x_val, gps.y_val, gps.z_val, ori.w_val, ori.x_val, ori.y_val, ori.z_val])
            print(f"Captured {filename}")

    # FLIGHT PATH: Dual Orbit (Industry Standard Photogrammetry)
    # Orbit 1: Outer wide circle
    radius_1 = 30
    alt_1 = -20
    print(f"Starting Outer Orbit (Radius {radius_1}m, Alt {abs(alt_1)}m)...")
    
    idx = 0
    for angle in range(0, 360, 15):
        rad = math.radians(angle)
        x = radius_1 * math.sin(rad)
        y = radius_1 * math.cos(rad)
        yaw = math.degrees(math.atan2(-y, -x))  # Look at center
        
        client.moveToPositionAsync(x, y, alt_1, 5).join()
        client.rotateToYawAsync(yaw).join()
        time.sleep(0.5) # Let drone stabilize to avoid blur
        capture_frame(idx)
        idx += 1

    # Orbit 2: Inner tight circle
    radius_2 = 15
    alt_2 = -12
    print(f"Starting Inner Orbit (Radius {radius_2}m, Alt {abs(alt_2)}m)...")
    
    for angle in range(0, 360, 20):
        rad = math.radians(angle)
        x = radius_2 * math.sin(rad)
        y = radius_2 * math.cos(rad)
        yaw = math.degrees(math.atan2(-y, -x))  # Look at center
        
        client.moveToPositionAsync(x, y, alt_2, 3).join()
        client.rotateToYawAsync(yaw).join()
        time.sleep(0.5)
        capture_frame(idx)
        idx += 1

    csv_file.close()
    
    print("Scan complete! Returning home...")
    client.moveToPositionAsync(0, 0, -10, 5).join()
    client.landAsync().join()
    client.armDisarm(False)
    client.enableApiControl(False)
    print("Drone secured.")

if __name__ == "__main__":
    main()


