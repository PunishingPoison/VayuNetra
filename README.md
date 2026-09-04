# VayuNetra

[ INSERT PROJECT SCREENSHOT HERE ]

## Overview
VayuNetra is an end-to-end, fully localized 3D Gaussian Splatting pipeline designed to generate photorealistic 3D models using synthetic drone data. 

By leveraging Unreal Engine 5, AirSim, and Python, VayuNetra automates the complex flight patterns required for professional photogrammetry. The captured high-definition video is then processed locally using Jawset Postshot and rendered seamlessly in Blender.

## Technologies Used
* **Unreal Engine 5:** High-fidelity simulation and environment rendering.
* **Microsoft AirSim:** Synthetic drone simulation and flight physics.
* **Python & OpenCV:** Custom automated flight controllers, video processing, and manual WASD overrides.
* **Jawset Postshot:** Lightning-fast, local 3D Gaussian Splatting (SfM and Training).
* **Blender & Kiri Engine Add-on:** Final 3D scene compositing, cropping, and rendering.

---

## Key Features & Scripts

VayuNetra includes several advanced flight controllers tailored for different 3D scanning scenarios:

### 1. Automated Neighborhood Patrol (Figure-8)
* **Script:** `scripts/record_street_video.py` (or `Launch_Automated_Patrol.bat`)
* Flies a massive, perfectly smooth continuous Figure-8 (Lemniscate) pattern at 2.5-stories high. Keeps the camera tilted to thoroughly capture streets and building facades. 

### 2. Custom WASD Manual Controller
* **Script:** `scripts/record_manual_wasd.py` (or `Launch_Drone_Controller.bat`)
* Bypasses Unreal Engine's native keyboard focus bugs. Provides a reliable, API-driven OpenCV window to manually fly the drone using standard PC gaming controls (W/A/S/D) while silently recording 1080p video.

### 3. Object-Centric 3D Spiral
* **Script:** `scripts/record_object_spiral.py`
* Executes a cinematic, ascending 3D corkscrew spiral around a central point of interest. It dynamically calculates and adjusts the camera pitch and yaw in real-time to keep the target perfectly framed.

### 4. Procedural Asset Generator
* **Script:** `scripts/create_tower.py`
* Instantly generates a highly detailed, 24-meter tall procedural Sci-Fi Tower (`.obj`) to serve as an instant scanning target in an empty environment.

---

## Installation & Setup

### 1. Prerequisites
* **Unreal Engine 5** (with your desired environment loaded)
* **Jawset Postshot** (for 3DGS training)
* **Blender** (for final rendering)
* **Miniconda / Anaconda**

### 2. Environment Setup
Clone the repository and set up the Python environment:
```bash
git clone https://github.com/PunishingPoison/VayuNetra.git
cd VayuNetra
conda create -n vayunetra python=3.9
conda activate vayunetra
pip install msgpack-rpc-python airsim opencv-python numpy
```

### 3. Configure AirSim for 1080p
To ensure maximum quality for the Gaussian Splat AI, force AirSim to record in 1080p. 
Navigate to `C:\Users\YOUR_NAME\OneDrive\Documents\AirSim\settings.json` (or your local Documents folder) and update it:
```json
{
  "SettingsVersion": 1.2,
  "SimMode": "Multirotor",
  "CameraDefaults": {
    "CaptureSettings": [
      {
        "ImageType": 0,
        "Width": 1920,
        "Height": 1080,
        "FOV_Degrees": 90
      }
    ]
  }
}
```
*(Restart your Unreal Engine simulation for this to take effect).*

---

## Pipeline Workflow (How to Use)

[ INSERT WORKFLOW/RESULTS SCREENSHOT HERE ]

**Step 1: Record the Flight**
Start your Unreal Engine simulation. Open your terminal, activate the `vayunetra` environment, and run the automated patrol:
```bash
python scripts/record_street_video.py
```
*(Alternatively, just double-click `Launch_Automated_Patrol.bat` from Windows Explorer).*

**Step 2: Train the AI (Postshot)**
* Locate your recorded video at `data/raw_video/neighborhood_patrol_1080p.mp4`.
* Drag and drop the `.mp4` into **Jawset Postshot**.
* *Tip:* Reduce the frame extraction rate (e.g., skip every 5 frames) to speed up training.
* Click **Train**. Once the model is sharp, click **Export -> .ply**.

**Step 3: Render (Blender)**
* Open Blender and ensure the **Kiri Engine 3DGS Add-on** is installed and enabled.
* Press `N` to open the side panel, go to the 3DGS tab, and click **Import .PLY**.
* Use the add-on's cropping tools to delete any "floaters" or sky artifacts.

---
## Pro Tips for Gaussian Splatting
* **The "Game Sky" Problem:** Video game skies are infinitely far away, which confuses SfM algorithms. Use Postshot's bounding box tool before training to crop out the sky and force the AI to focus strictly on the buildings.
* **Motion Blur:** Drones snapping to waypoints cause motion blur, ruining photogrammetry. This is why VayuNetra utilizes continuous velocity vectors (`moveByVelocityAsync`) to guarantee buttery-smooth footage.

