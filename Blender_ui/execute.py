# Blender operator class to execute the node graph
#### Blender Import ####
import bpy

# class MajaxExecuteOperator(bpy.types.Operator):
#     """Tooltip"""
#     bl_idname = "object.execute_operator"
#     bl_label = "Majax Execute Operator"
# 
#     # @classmethod
#     # def poll(cls, context):
#     #     return context.active_object is not None
# 
#     def execute(self, context):
#         print(self)
#         print(context)
#         print(*context.__dict__.items(), sep="\n")
#         return {'FINISHED'}
class MajaxExecuteOperator(bpy.types.Operator):
    """Run the Simulation graph computation"""
    bl_idname = "majax.execute_node_tree"
    bl_label = "Majax Execute Operator"

    def execute(self, context):
        # Poll already dones in the button layout
        nodetree = context.space_data.node_tree
        if True: # context.tool_settings.restart:
            start_frame = context.scene.frame_current
            context.scene.frame_current = start_frame
        else:
            start_frame = context.scene.frame_current
        end_frame = context.scene.frame_end

        print("\nExecute Majax Graph")
        print("Get nodetree: ", context.space_data.node_tree.name)
        print("frame:", start_frame, "--", end_frame)

        nodetree.execute(start_frame, end_frame)

        return {'FINISHED'}

class MajaxCompileOperator(bpy.types.Operator):
    """Compile all kernels"""
    bl_idname = "majax.compile_node_tree"
    bl_label = "Majax Compile Operator"

    def execute(self, context):
        # Poll already dones in the button layout
        nodetree = context.space_data.node_tree
        print("Compile")

        nodetree.compile()

        return {'FINISHED'}
