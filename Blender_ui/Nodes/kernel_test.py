from .base_node import BaseNode
from bpy.types import Node
from bpy.props import EnumProperty, PointerProperty, IntProperty

# Make automatique construction of the enum_list from OpenCL device
class KernelTestNode(BaseNode, Node):
    '''Execute the Test script Kernel'''
    # Optional identifier string.
    bl_idname = 'KernelTestNode'
    # Label for nice name display
    bl_label = "Kernel Test"
    # Operator reference that is associate with the node
    operator = "BlKernelTestOperator"

    # === Properties ===
    work_group_size: IntProperty(default=256, min=0, name="Kernel size")
    size: IntProperty(name="Kernel_size")

    def init(self, context):
        self.name = self.bl_label.replace(" ", "_")
        self.inputs.new("MajaxSocketBuffers", "Buffer")
        self.inputs[-1].intent = "inout"
        self.outputs.new('MajaxSocketBuffers', "Buffer")
        self.outputs[-1].intent = "inout"

    def update(self):
        """Executed when a new link is made. Delete Unconnected virtual socket"""
        pass

    # Properterties edition on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, "work_group_size")

    # Properties interface on the sidebar.
    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "work_group_size")