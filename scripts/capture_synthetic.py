import os
import time
import json
import csv
import math
import airsim

def main():
    print("Connecting to Colosseum/AirSim...")
    # Connect to the AirSim simulator
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)

    # Setup directories
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    raw_dir = os.path.join(base_dir, 'raw')
    telemetry_file = os.path.join(raw_dir, 'telemetry.csv')
    os.makedirs(raw_dir, exist_ok=True)

    print("Taking off...")
    client.takeoffAsync().join()

    print("Gaining altitude...")
    # Move straight up 15 meters to clear trees/houses
    client.moveToZAsync(-15, 3).join()
    
    print("Starting single-pass capture...")
    
    # Fly straight forward (X-axis) at 4 meters per second for 15 seconds
    fly_duration = 15.0
    client.moveByVelocityAsync(4, 0, 0, fly_duration)
    
    # Open telemetry CSV
    with open(telemetry_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'image_name', 'lat', 'lon', 'alt', 'qw', 'qx', 'qy', 'qz'])
        
        frame_idx = 0
        start_time = time.time()
        
        # Capture frames while moving
        while (time.time() - start_time) < fly_duration:
            # Request image and kinematics (set compress=True to get valid PNG bytes)
            responses = client.simGetImages([
                airsim.ImageRequest("0", airsim.ImageType.Scene, False, True)
            ])
            kinematics = client.simGetGroundTruthKinematics()
            gps = client.getMultirotorState().gps_location
            
            if len(responses) > 0:
                img_response = responses[0]
                img_name = f"frame_{frame_idx:05d}.png"
                img_path = os.path.join(raw_dir, img_name)
                
                # Save image
                airsim.write_file(img_path, img_response.image_data_uint8)
                
                # Record telemetry
                ts = time.time()
                writer.writerow([
                    ts,
                    img_name,
                    gps.latitude,
                    gps.longitude,
                    gps.altitude,
                    kinematics.orientation.w_val,
                    kinematics.orientation.x_val,
                    kinematics.orientation.y_val,
                    kinematics.orientation.z_val
                ])
                print(f"Captured {img_name}")
                frame_idx += 1
                
            # Sleep to hit roughly target FPS (e.g., 5 FPS)
            time.sleep(0.2)

    print("Flyby complete. Landing...")
    client.landAsync().join()
    client.armDisarm(False)
    client.enableApiControl(False)
    print(f"Capture complete. Data saved to {raw_dir}")

if __name__ == '__main__':
    main()
