# Unreal Engine Setup Guide

## SplatRenderer Integration
1. The `SplatRenderer` plugin is cloned into `unreal/Plugins/SplatRenderer`.
2. Right-click `VayuNetra.uproject` and generate Visual Studio project files (if you have added C++ code), or just double click to open it and let it build the plugin.

## Required Blueprints (To be built in editor)

Since Unreal uses binary `.uasset` files, create the following Blueprints manually in the editor:

### 1. `BP_SplatSceneActor`
- **Parent Class**: `Actor`
- **Components**: Add `NiagaraComponent` (configured for Gaussian Splats via the SplatRenderer plugin).
- **Logic**: In `BeginPlay`, read `manifests/transform.json` to apply the correct scale and rotation to the splat actor so it aligns with real-world ENU coordinates.

### 2. `BP_TelemetryOverlay`
- **Parent Class**: `Actor`
- **Components**: `SplineComponent`
- **Logic**: Read `data/raw/telemetry.csv` and populate the spline points to visualize the drone's flight path above the splat.

### 3. `BP_MeasurementTool`
- **Parent Class**: `PlayerController` or `Widget`
- **Logic**: Line trace against the Splat geometry (or proxy collision). On first click, save `StartLocation`. On second click, save `EndLocation`. Calculate `VectorLength(Start, End)` and display it in UI in meters.
