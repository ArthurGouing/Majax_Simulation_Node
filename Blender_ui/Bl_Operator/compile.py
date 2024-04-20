#### Blender Import ####
import bpy

class MajaxCompileOperator(bpy.types.Operator):
    """Compile all kernels"""
    bl_idname = "majax.compile_node_tree"
    bl_label = "Majax Compile Operator"

    def execute(self, context):
        # Poll already dones in the button layout
        nodetree = context.space_data.node_tree
        # Update node tree to the scene
        context.scene.majax_node_tree = nodetree

        print("Compile")
        nodetree.compile()

        return {'FINISHED'}