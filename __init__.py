bl_info = {
    "name": "IC-LIGHT blender",
    "author": "Xiangyi Gao",
    "version": (1, 0),
    "blender": (4, 2, 0),
    "location": "Preferences",
    "description": "",
    "doc_url": "https://github.com/xy-gao/IC-Light-Blender",
}


import bpy
from bpy.types import AddonPreferences, Operator, Panel
import sys
import os
from bpy.props import (StringProperty,
                       PointerProperty,
                       )
# Local imports
from .dependencies import Dependencies

class EXAMPLE_OT_install_dependencies(Operator):
    bl_idname = "preferences.example_install_dependencies"
    bl_label = "Install dependencies"
    bl_description = ("Downloads and installs the required Python packages for this add-on. "
                      "Internet connection is required. Packages are installed locally to "
                      "this add-on, not to the system Python or Blender's Python.")
    bl_options = {"REGISTER", "INTERNAL"}

    @classmethod
    def poll(self, context):
        # Deactivate when dependencies have been installed
        return not Dependencies.check()

    def execute(self, context):
        if not Dependencies.install():
            return {'CANCELLED'}

        # Register any classes that need registering once dependencies are installed
        print(f"-----------------check{Dependencies.check()}")
        register_classes_with_dependencies()

        return {"FINISHED"}


class EXAMPLE_AddonPreferences(AddonPreferences):
    """ Preferences for this dummy add-on """
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout

        # layout.label(text=f"This add-on requires a couple Python packages to be installed:")
        # for name in Dependencies.requirements():
        #     layout.label(text=f'- {name}')

        layout.label(text=f"Click the Install Dependencies button below to install.")
        layout.operator(EXAMPLE_OT_install_dependencies.bl_idname, icon="CONSOLE")




registered_classes_with_dependencies = False

classes_example = [
    EXAMPLE_OT_install_dependencies,
    EXAMPLE_AddonPreferences,

]

def register_classes_with_dependencies():
    from .panel import PromptProperties, ICLightPanel
    from .relight import Relight

    global registered_classes_with_dependencies
    if registered_classes_with_dependencies:
        # Already registered classes
        return

    if not Dependencies.check(force=True):
        # Dependencies are not installed, so cannot register the classes
        return
    classes_with_dependencies = [
        PromptProperties,
        ICLightPanel,
        Relight
    ]
    for cls in classes_with_dependencies:
        bpy.utils.register_class(cls)

    bpy.types.Scene.prompts = PointerProperty(type=PromptProperties)
    registered_classes_with_dependencies = True

def unregister_classes_with_dependencies():
    from .panel import PromptProperties, ICLightPanel
    from .relight import Relight

    global registered_classes_with_dependencies
    if not registered_classes_with_dependencies:
        # No registered classes needing unregistered
        return
    classes_with_dependencies = [
        PromptProperties,
        ICLightPanel,
        Relight
    ]
    for cls in reversed(classes_with_dependencies):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.prompts
    registered_classes_with_dependencies = False

def register():
    for cls in classes_example:
        bpy.utils.register_class(cls)
    if Dependencies.check():
        register_classes_with_dependencies()




def unregister():
    if Dependencies.check():
        unregister_classes_with_dependencies()
    for cls in reversed(classes_example):
        bpy.utils.unregister_class(cls)

