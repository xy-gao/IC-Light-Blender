import bpy
import numpy as np
from  .gradio_demo import process_relight


def process(input_img, prompt, light_position):

    input_fg = input_img[:,:,:-1]
    input_a = input_img[:,:,-1]
    # prompt = "prompt"
    image_width = int(input_fg.shape[1] /2)
    image_height = int(input_fg.shape[0] /2)
    # image_width = 512
    # image_height = 640
    num_samples = 1
    seed = 12345
    steps = 25
    a_prompt = 'best quality'
    n_prompt = 'lowres, bad anatomy, bad hands, cropped, worst quality'
    cfg = 2
    highres_scale = 1.5
    highres_denoise = 0.5
    lowres_denoise = 0.9
    bg_source = light_position

    output_bg, result_gallery = process_relight(input_fg, input_a, prompt, image_width, image_height, num_samples, seed, steps, a_prompt, n_prompt, cfg, highres_scale, highres_denoise, lowres_denoise, bg_source)
    return result_gallery[0]

def reshape_array(array):
    """Reshapes a 1D array of length 8294400 into a 1920x1080x4 array.

    Args:
        array: A 1D NumPy array of length 8294400.

    Returns:
        A 3D NumPy array of shape (1920, 1080, 4), representing a 1920x1080 RGBA image.
    """

    # Reshape the array into a 3D array
    image_array = array.reshape(bpy.context.scene.render.resolution_y, bpy.context.scene.render.resolution_x, 4)

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
    rgba_image = np.ones((height, width, 4), dtype=numpy_array.dtype)

    # Copy the RGB channels
    rgba_image[:, :, :3] = numpy_array
    # Create a new Blender image
    image = bpy.data.images.new(name="NumpyImage", width=width, height=height)

    # Flatten the NumPy array and assign it to the image pixels
    print(rgba_image)
    image.pixels.foreach_set(rgba_image.flatten())

    return image
 

class Relight(bpy.types.Operator):
    """Relight"""

    bl_idname = "render.ic"
    bl_label = "Relight"
    bl_options = {"REGISTER", "UNDO"}


    def execute(self, context):
        
        bpy.context.scene.render.film_transparent = True
        bpy.context.scene.view_settings.view_transform = 'Raw'

        scene = context.scene
        prompts = scene.prompts

        print(prompts.object)
        print(prompts.light_environment)
        print(prompts.light_position)
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
        

        c = tree.nodes.new('CompositorNodeComposite')   
        c.location = 750,100
        c.use_alpha = True


        # Links
        links.new(rl.outputs[0], v.inputs[0])  # link Image output to Viewer input
        links.new(rl.outputs[0], c.inputs[0])
        # render
        bpy.ops.render.render()
        
        # get viewer pixels
        pixels = bpy.data.images['Viewer Node'].pixels
        print(len(pixels)) # size is always width * height * 4 (rgba)
        
        # copy buffer to numpy array for faster manipulation
        arr = np.array(pixels[:])

        # Example usage:
        # Assuming you have a 1D array named 'data' with length 8294400
        image_array = np.flipud(reshape_array(arr))*255


        image_array = process(image_array.astype(np.uint8), f"{prompts.object}, {prompts.light_environment}", prompts.light_position)

        res_pixels = np.flipud(image_array/255)
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



        return {"FINISHED"}


def register():
    bpy.utils.register_class(Relight)


def unregister():
    bpy.utils.unregister_class(Relight)


if __name__ == "__main__":
    register()