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
    
    # Tilt camera down slightly to see the road and houses
    print("Tilting camera down 20 degrees for street view...")
    pitch = -math.radians(20)
    client.simSetCameraPose("0", airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(pitch, 0, 0)))
    time.sleep(1)
    
    # Flight Parameters
    altitude = -8.0      # Low altitude (about 8 meters / 2.5 stories high)
    scale_x = 40.0       # 80 meter total width
    scale_y = 40.0       # 80 meter total length
    duration = 60.0      # 60 second flight
    
    print("Moving to start of the street patrol route...")
    client.moveToPositionAsync(0, 0, altitude, 5).join()
    
    # Initialize OpenCV Video Writer
    response = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])[0]
    width, height = response.width, response.height
    
    video_path = os.path.join(raw_dir, 'neighborhood_patrol_1080p.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_path, fourcc, 30.0, (width, height))
    
    print(f"RECORDING HIGH-RES {width}x{height} VIDEO to {video_path}")
    print("Flying sweeping Figure-8 patrol route... please wait.")
    
    start_time = time.time()
    frames_recorded = 0
    
    while True:
        t = time.time() - start_time
        if t > duration:
            break
            
        # Lissajous Figure-8 Curve for smooth, continuous neighborhood sweeping
        omega = (2 * math.pi) / duration
        theta = omega * t
        
        # Calculate velocities (derivatives of position)
        vx = scale_x * omega * math.cos(theta)
        vy = scale_y * 2 * omega * math.cos(2 * theta)
        vz = 0
        
        # Point the drone exactly where it is flying (forward street view)
        yaw = math.degrees(math.atan2(vy, vx))
        
        # Send continuous velocity command
        client.moveByVelocityAsync(vx, vy, vz, 0.5, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, yaw))
        
        # Capture Frame
        resp = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])[0]
        img1d = np.frombuffer(resp.image_data_uint8, dtype=np.uint8)
        img_rgb = img1d.reshape(resp.height, resp.width, 3)
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        
        out.write(img_bgr)
        frames_recorded += 1
        
    out.release()
    print(f"Recording complete! Saved {frames_recorded} high-res frames to {video_path}")
    
    print("Returning home...")
    client.moveToPositionAsync(0, 0, -10, 5).join()
    client.landAsync().join()
    client.armDisarm(False)
    client.enableApiControl(False)
    print("Drone secured.")

if __name__ == "__main__":
    main()
