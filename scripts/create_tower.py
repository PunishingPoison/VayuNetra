import math
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
obj_filepath = os.path.join(base_dir, "futuristic_tower.obj")

vertices = []
faces = []

# Tower parameters (Height and Radius at that height)
# Creates a wide base, sweeping curves, a command deck, and a sharp spire
profile = [
    (0, 5),     # Ground base
    (1, 4.8), 
    (3, 4),
    (6, 2.5),
    (12, 1.5),  # Slender neck
    (13, 1.5),
    (14, 3.5),  # Command deck bulges out
    (15, 3.5),
    (16, 1.5),
    (18, 1.0),
    (24, 0.0)   # Sharp spire tip at 24 meters
]
segments = 64

# Generate Vertices
for h, r in profile:
    for j in range(segments):
        angle = (2 * math.pi * j) / segments
        # Add some geometric ridges (star shape)
        ridge = 1.0 + 0.1 * math.sin(angle * 8)
        x = r * ridge * math.cos(angle)
        y = r * ridge * math.sin(angle)
        vertices.append((x, y, h))

# Generate Faces
for i in range(len(profile) - 1):
    for j in range(segments):
        next_j = (j + 1) % segments
        
        # Current ring
        p1 = i * segments + j + 1
        p2 = i * segments + next_j + 1
        
        # Next ring
        p3 = (i + 1) * segments + j + 1
        p4 = (i + 1) * segments + next_j + 1
        
        faces.append((p1, p2, p3))
        faces.append((p2, p4, p3))

# Close the base
center_idx = len(vertices) + 1
vertices.append((0, 0, 0))
for j in range(segments):
    next_j = (j + 1) % segments
    faces.append((center_idx, next_j + 1, j + 1))

with open(obj_filepath, "w") as f:
    f.write("# Procedural Sci-Fi Tower\n")
    for v in vertices:
        f.write(f"v {v[0]} {v[1]} {v[2]}\n")
    for face in faces:
        f.write(f"f {face[0]} {face[1]} {face[2]}\n")

print(f"Created 3D Model: {obj_filepath}")
