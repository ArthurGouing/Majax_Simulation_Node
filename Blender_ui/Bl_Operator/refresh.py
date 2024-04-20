# Blender operator class to execute the node graph
#### Blender Import ####
import bpy

class MajaxRefreshOperator(bpy.types.Operator):
    """Run the Simulation graph computation"""
    bl_idname = "majax.refresh_node_tree"
    bl_label = "Majax Refresh Operator"

    def execute(self, context):
        # Poll already dones in the button layout
        context.scene.frame_current = context.scene.frame_start
        bpy.ops.screen.animation_play()

        return {'FINISHED'}
