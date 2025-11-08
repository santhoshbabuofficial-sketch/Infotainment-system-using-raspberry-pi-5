import open3d as o3d

# Path to your GLB file
model_path = r"D:\infotainment system\3d model\smart electric bicycle fixed.glb"

# Initialize the GUI application
o3d.visualization.gui.Application.instance.initialize()

# Create a window
window = o3d.visualization.gui.Application.instance.create_window("3D Model Viewer", 800, 600)

# Create a scene widget
scene_widget = o3d.visualization.gui.SceneWidget()
scene_widget.scene = o3d.visualization.rendering.Open3DScene(window.renderer)

# Load GLB model with materials and textures
model = o3d.io.read_triangle_model(model_path)
scene_widget.scene.add_model("model", model)

# Setup camera
bounds = scene_widget.scene.bounding_box
scene_widget.setup_camera(40, bounds, bounds.get_center())

# Add scene widget to the window
window.add_child(scene_widget)

# Run the GUI app
o3d.visualization.gui.Application.instance.run()
