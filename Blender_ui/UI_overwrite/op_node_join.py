# Rewrite bpy.ops.node.join()
# To add color, name and correct size to the node label
import bpy
from mathutils import Color

# cd templtes operator_node.py

def new_join_ops(Operator):
    def action(self, context):
        bpy.ops.node.join()
        # after join operation, the active node is the newly created frame
        # 1
        new_frame = operator.selected_nodes
        new_frame.color = Color((.25, .25, .25))
        new_frame.use_custom_color = True
        new_frame.label_size = 20 # IDEM
        new_frame.label = "Name"  # Make a property so the user can choose the node name
