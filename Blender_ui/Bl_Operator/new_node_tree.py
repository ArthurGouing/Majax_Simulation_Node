#### Blender Import ####
import bpy

class MajaxAddNodeTreeOperator(bpy.types.Operator):
    """Run the Simulation graph computation"""
    bl_idname = "majax.new_node_tree"
    bl_label = "Majax New Node Tree Operator"

    def execute(self, context):
        # Create a new majax node tree
        name = "Majax_Simulation_Node"
        node_tree = bpy.data.node_groups.new(name, "CustomTreeType")

        # Set scene node graph
        context.scene.majax_node_tree = node_tree

        # Set node editor window node graph
        context.space_data.node_tree = node_tree


        return {'FINISHED'}

