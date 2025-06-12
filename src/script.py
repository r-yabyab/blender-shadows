import bpy
import math
import os

# Parameters
shadow_angles = [0, 45, 90, 135, 180]  # Azimuth (Z rotation)
elevations = [15, 45, 75]             # Elevation (X rotation)
#intensities = [1.0, 3.0, 5.0]          # Light intensity

# Save path
save_path = "C:/Users/cayab/Desktop/blender1/viewport_renders"
os.makedirs(save_path, exist_ok=True)

# Get or create Sun light
sun_name = "Sun_Light"
sun = bpy.data.objects.get(sun_name)
if not sun:
    light_data = bpy.data.lights.new(name=sun_name, type='SUN')
    sun = bpy.data.objects.new(name=sun_name, object_data=light_data)
    bpy.context.collection.objects.link(sun)

sun.rotation_mode = 'XYZ'

# Function to set sun rotation only
def configure_sun(elevation_deg, azimuth_deg):
    sun.rotation_euler = (
        math.radians(elevation_deg),
        0,
        math.radians(azimuth_deg)
    )
    # sun.data.energy = intensity  # Commented out

# Nested loop for combinations (elevation + azimuth only)
for elevation in elevations:
    for azimuth in shadow_angles:
        configure_sun(elevation, azimuth)
        bpy.context.view_layer.update()

        # Viewport render
        bpy.ops.render.opengl(write_still=True)
        render_result = bpy.data.images.get("Render Result")
        if render_result:
            filename = f"viewport_elev{elevation}_az{azimuth}.png"
            filepath = os.path.join(save_path, filename)
            render_result.save_render(filepath)
            print(f"Saved: {filepath}")

print("All renders completed.")
