import bpy
import numpy as np


def reshape_array(array):
  """Reshapes a 1D array of length 8294400 into a 1920x1080x4 array.

  Args:
    array: A 1D NumPy array of length 8294400.

  Returns:
    A 3D NumPy array of shape (1920, 1080, 4), representing a 1920x1080 RGBA image.
  """

  # Check if the input array has the correct length
  if len(array) != 8294400:
    raise ValueError("Input array must have length 8294400.")

  # Reshape the array into a 3D array
  image_array = array.reshape(1080, 1920, 4)

  # Transpose the array to get the correct order of dimensions (height, width, channels)
  image_array = image_array.transpose(0, 1, 2)

  return image_array


def numpy_to_blender_image(numpy_array):
    """Converts a NumPy array to a Blender image.

    Args:
        numpy_array: The NumPy array representing the image.

    Returns:
        The created Blender image.
    """

    # Ensure the NumPy array is in the correct format (float32)
    if numpy_array.dtype != np.float32:
        numpy_array = numpy_array.astype(np.float32)

    # Get image dimensions and channels
    height, width, channels = numpy_array.shape

    # Create a new Blender image
    image = bpy.data.images.new(name="NumpyImage", width=width, height=height)

    # Flatten the NumPy array and assign it to the image pixels
    print(numpy_array)
    image.pixels.foreach_set(numpy_array.flatten())

    return image


# switch on nodes
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree
links = tree.links
  
# clear default nodes
for n in tree.nodes:
    tree.nodes.remove(n)
  
# create input render layer node
rl = tree.nodes.new('CompositorNodeRLayers')      
rl.location = 185,285
 
# create output node
v = tree.nodes.new('CompositorNodeViewer')   
v.location = 750,210
v.use_alpha = True
 
# Links
links.new(rl.outputs[0], v.inputs[0])  # link Image output to Viewer input
 
# render
bpy.ops.render.render()
 
# get viewer pixels
pixels = bpy.data.images['Viewer Node'].pixels
print(len(pixels)) # size is always width * height * 4 (rgba)
 
# copy buffer to numpy array for faster manipulation
arr = np.array(pixels[:])

# Example usage:
# Assuming you have a 1D array named 'data' with length 8294400
image_array = np.flipud(reshape_array(arr))


#do some

res_pixels = np.flipud(image_array)
print(len(res_pixels))

# Example usage:
# Assuming you have a NumPy array named 'numpy_image'
blender_image = numpy_to_blender_image(res_pixels)

# Call user prefs window
bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
# Change area type
area = bpy.context.window_manager.windows[-1].screen.areas[0]
area.type = 'IMAGE_EDITOR'

for area in bpy.context.screen.areas:
    if area.type == 'IMAGE_EDITOR':
        area.spaces.active.image = blender_image

