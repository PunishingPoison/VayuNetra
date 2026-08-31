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

    # Move to starting position (e.g., higher altitude)
    print("Moving to start position...")
    client.moveToPositionAsync(0, 0, -20, 5).join()
    
    # We will fly a straight line pass over the scene
    start_pt = airsim.Vector3r(0, -50, -20)
    end_pt = airsim.Vector3r(0, 50, -20)
    velocity = 3.0 # m/s
    
    client.moveToPositionAsync(start_pt.x_val, start_pt.y_val, start_pt.z_val, velocity).join()
    
    print("Starting single-pass capture...")
    
    # Start the actual flyby pass asynchronously
    fly_task = client.moveToPositionAsync(end_pt.x_val, end_pt.y_val, end_pt.z_val, velocity)
    
    # Open telemetry CSV
    with open(telemetry_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'image_name', 'lat', 'lon', 'alt', 'qw', 'qx', 'qy', 'qz'])
        
        frame_idx = 0
        
        # Capture frames while moving
        while not fly_task.is_done():
            # Request image and kinematics
            responses = client.simGetImages([
                airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)
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
