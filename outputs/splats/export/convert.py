import plyfile
import numpy as np

print("Loading PLY...")
plydata = plyfile.PlyData.read(r'outputs\splats\export\splat.ply')
v = plydata['vertex']

x = v['x']
y = v['y']
z = v['z']

SH_C0 = 0.28209479177387814
r = np.clip((v['f_dc_0'] * SH_C0 + 0.5) * 255.0, 0, 255).astype(np.uint8)
g = np.clip((v['f_dc_1'] * SH_C0 + 0.5) * 255.0, 0, 255).astype(np.uint8)
b = np.clip((v['f_dc_2'] * SH_C0 + 0.5) * 255.0, 0, 255).astype(np.uint8)

print("Writing TXT...")
out_data = np.column_stack((x, y, z, r, g, b))
np.savetxt(r'outputs\splats\export\splat.txt', out_data, fmt='%.6f %.6f %.6f %d %d %d')
print("Done!")
