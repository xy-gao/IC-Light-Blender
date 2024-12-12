import bpy
from bpy.props import (StringProperty,
                       PointerProperty,
                       )
                       
from bpy.types import (Panel,
                       PropertyGroup,
                       )
class PromptProperties(PropertyGroup):

    object: StringProperty(
        name="object",
        description=":",
        default="",
        maxlen=1024,
        )
    light_environment: StringProperty(
        name="light_environment",
        description=":",
        default="",
        maxlen=1024,
        )
    light_position: bpy.props.EnumProperty(
        items=[
            ('Left Light', "Left Light", ""),
            ('Right Light', "Right Light", ""),
            ('Top Light', "Top Light", ""),
            ('Bottom Light', "Bottom Light", "")
        ],
        name="My Enum"
    )

quick_prompts = [
    'sunshine from window',
    'neon light, city',
    'sunset over sea',
    'golden time',
    'sci-fi RGB glowing, cyberpunk',
]

class ICLightPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""

    bl_label = "IC"
    bl_idname = "OBJECT_PT_IC"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "IC"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prompts = scene.prompts

        layout.prop(prompts, "object")
        layout.prop(prompts, "light_environment")
        layout.label(text="example light_environment:")
        for i in quick_prompts:
            layout.label(text=i)
        layout.prop(prompts, "light_position", expand=True)
        # Create Eye
        layout.label(text="Relight:")
        row = layout.row()
        row.operator("render.ic")


def register():
    bpy.utils.register_class(ICLightPanel)
    bpy.utils.register_class(PromptProperties)
    bpy.types.Scene.prompts = PointerProperty(type=PromptProperties)

def unregister():
    bpy.utils.unregister_class(ICLightPanel)
    bpy.utils.unregister_class(PromptProperties)
    del bpy.types.Scene.prompts

if __name__ == "__main__":
    register()