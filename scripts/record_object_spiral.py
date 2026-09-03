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
    
    # ---------------------------------------------------------
    # OBJECT SCANNING PARAMETERS
    # ---------------------------------------------------------
    radius = 12.0          # How far away to stay from the object (meters)
    start_alt = -2.0       # Start low (2 meters above ground)
    end_alt = -15.0        # End high (15 meters above ground)
    duration = 60.0        # Total video length (60 seconds)
    revolutions = 3.0      # Number of full circles around the object
    
    print(f"Moving to spiral start position (Radius {radius}m, Alt {abs(start_alt)}m)...")
    client.moveToPositionAsync(radius, 0, start_alt, 5).join()
    
    # Initialize OpenCV Video Writer
    response = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])[0]
    width, height = response.width, response.height
    video_path = os.path.join(raw_dir, 'object_scan_spiral.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_path, fourcc, 30.0, (width, height))
    
    print(f"RECORDING 3D SPIRAL VIDEO to {video_path}")
    print("Starting cinematic spiral. The camera will auto-track the object...")
    
    start_time = time.time()
    frames_recorded = 0
    
    while True:
        t = time.time() - start_time
        if t > duration:
            break
            
        # 1. Calculate Spiral Math
        omega = (revolutions * 2 * math.pi) / duration # Rotation speed
        theta = omega * t
        
        # Calculate current height (linear interpolation from start_alt to end_alt)
        current_z = start_alt + ((end_alt - start_alt) * (t / duration))
        
        # 2. Calculate Velocities (X, Y tangent to circle, Z climbing)
        v_mag = radius * omega
        vx = -v_mag * math.sin(theta)
        vy = v_mag * math.cos(theta)
        vz = (end_alt - start_alt) / duration
        
        # 3. Dynamic Camera Tracking (Always look at center 0,0,0)
        yaw = math.degrees(theta) + 180.0
        
        # Dynamic Pitch: As drone gets higher (more negative Z), pitch tilts down
        # atan2(Z, Radius) automatically gives us the perfect negative pitch angle in radians
        pitch_rad = math.atan2(current_z, radius) 
        
        # Apply the pitch to the gimbal
        client.simSetCameraPose("0", airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(pitch_rad, 0, 0)))
        
        # Send movement command
        client.moveByVelocityAsync(vx, vy, vz, 0.5, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, yaw))
        
        # 4. Capture Frame for Video
        resp = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])[0]
        img1d = np.frombuffer(resp.image_data_uint8, dtype=np.uint8)
        img_rgb = img1d.reshape(resp.height, resp.width, 3)
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        
        out.write(img_bgr)
        frames_recorded += 1
        
    out.release()
    print(f"Recording complete! Saved {frames_recorded} frames to {video_path}")
    
    print("Returning home...")
    client.simSetCameraPose("0", airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(0, 0, 0))) # Reset camera
    client.moveToPositionAsync(0, 0, -10, 5).join()
    client.landAsync().join()
    client.armDisarm(False)
    client.enableApiControl(False)
    print("Drone secured.")

if __name__ == "__main__":
    main()
