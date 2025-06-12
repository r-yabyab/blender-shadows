import bpy
import math
import os

# Angles in degrees for light rotation around Z axis
shadow_angles = [0, 45, 90, 135, 180]

# Folder to save viewport renders
save_path = "C:/Users/cayab/Desktop/blender1/viewport_renders"
os.makedirs(save_path, exist_ok=True)

# Find or create a Sun light
sun_name = "Sun_Light"
sun = bpy.data.objects.get(sun_name)
if not sun:
    light_data = bpy.data.lights.new(name=sun_name, type='SUN')
    sun = bpy.data.objects.new(name=sun_name, object_data=light_data)
    bpy.context.collection.objects.link(sun)
    sun.rotation_mode = 'XYZ'

sun.rotation_mode = 'XYZ'

def set_sun_rotation_z(degrees):
    radians = math.radians(degrees)
    sun.rotation_euler = (math.radians(45), 0, radians)

def get_unique_filepath(base_dir, base_name, ext):
    counter = 1
    while True:
        suffix = f"_{counter:03d}"
        full_name = f"{base_name}{suffix}.{ext}"
        full_path = os.path.join(base_dir, full_name)
        if not os.path.exists(full_path):
            return full_path
        counter += 1

for angle in shadow_angles:
    set_sun_rotation_z(angle)
    bpy.context.view_layer.update()

    # Render viewport (OpenGL / material preview)
    bpy.ops.render.opengl(write_still=True)

    # Save the render result
    render_result = bpy.data.images.get("Render Result")
    if render_result:
        base_name = f"viewport_shadow_angle_{angle}"
        filepath = get_unique_filepath(save_path, base_name, "png")
        render_result.save_render(filepath)
        print(f"Saved: {filepath}")

print("All viewport renders saved.")
