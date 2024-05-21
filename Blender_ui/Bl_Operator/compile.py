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

        err_type, error_msg = nodetree.compile()

        # Print Compile in the Info Panel 
        if err_type=="warn_ker":
            self.report({'WARNING'}, "Warning raise while compiling kernels: \n" + error_msg)
        elif err_type=="err_ker":
            self.report({'ERROR'}, "Error while compiling kernels: \n" + error_msg)
        else:
            self.report({'OPERATOR'}, "Compiled Majax Graph Successfully")
        return {'FINISHED'}