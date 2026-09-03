import airsim
import time
import os
import math
import cv2
import numpy as np

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    raw_dir = os.path.join(base_dir, 'raw_video')
    if not os.path.exists(raw_dir):
        os.makedirs(raw_dir)
        
    print("Connecting to AirSim...")
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)
    
    print("Taking off...")
    client.takeoffAsync().join()
    
    print("Tilting camera down for 3D scanning...")
    pitch = -math.radians(35)
    client.simSetCameraPose("0", airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(pitch, 0, 0)))
    time.sleep(1)
    
    radius = 30
    altitude = -20
    orbit_duration = 30.0 # seconds for a full smooth circle
    
    print(f"Moving to start position (Radius {radius}m)...")
    client.moveToPositionAsync(radius, 0, altitude, 5).join()
    
    # Initialize OpenCV Video Writer
    print("Initializing camera...")
    response = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])[0]
    width, height = response.width, response.height
    
    video_path = os.path.join(raw_dir, 'drone_scan.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_path, fourcc, 30.0, (width, height))
    
    print(f"RECORDING VIDEO to {video_path}")
    print("Flying smooth orbit... please wait.")
    
    start_time = time.time()
    frames_recorded = 0
    
    while True:
        t = time.time() - start_time
        if t > orbit_duration:
            break
            
        # Math for smooth circular flight
        omega = (2 * math.pi) / orbit_duration
        theta = omega * t
        
        # Tangent velocity to orbit the center
        v_mag = radius * omega
        vx = -v_mag * math.sin(theta)
        vy = v_mag * math.cos(theta)
        
        # Keep camera locked on the center of the neighborhood
        yaw = math.degrees(theta) + 180.0
        
        client.moveByVelocityZAsync(vx, vy, altitude, 0.5, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, yaw))
        
        # Capture exact frame for video
        resp = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])[0]
        img1d = np.frombuffer(resp.image_data_uint8, dtype=np.uint8)
        img_rgb = img1d.reshape(resp.height, resp.width, 3)
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR) # Convert to OpenCV format
        
        out.write(img_bgr)
        frames_recorded += 1
        
    out.release()
    print(f"Recording complete! Saved {frames_recorded} frames to {video_path}")
    
    print("Returning home...")
    client.moveToPositionAsync(0, 0, -10, 5).join()
    client.landAsync().join()
    client.armDisarm(False)
    client.enableApiControl(False)
    print("Drone secured.")

if __name__ == "__main__":
    main()
