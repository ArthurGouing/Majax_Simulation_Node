import bpy
from .base_node import BaseNode
from bpy.types import Node
from bpy.props import PointerProperty, IntProperty


class KernelScriptNode(BaseNode, Node):
    '''Execute the choosen script Kernel'''
    # Optional identifier string.
    bl_idname = 'KernelScriptNode'
    # Label for nice name display
    bl_label = "Kernel Script"
    # Operator reference that is associate with the node
    operator = "BlOpenCLKernelOperator"

    # === Properties ===
    script: PointerProperty(type=bpy.types.Text, name="Script")
    work_group_size: IntProperty(default=256, min=0, name="Kernel size")

    def init(self, context):
        self.name = self.bl_label.replace(" ", "_")
        self.inputs.new('NodeSocketVirtual', "")
        self.outputs.new('NodeSocketVirtual', "")

    def update(self):
        """Executed when a new link is made. Delete Unconnected virtual socket"""
        # Could also update socket, by reading the script. / rename the node from the script name
        # Rename node
        # self.label = self.script.name.split(".")[0] #
        # Delte unused socket
        delta_socket = len(self.outputs) - len(self.inputs) # -1 car i commence à 1
        for i, socket in enumerate(self.inputs):
            if i>=len(self.inputs)-1:
                continue
            if not socket.is_linked:
                self.inputs.remove(socket)
        for i, socket in enumerate(self.outputs):
            if i>=len(self.outputs)-1:
                continue
            if not socket.is_linked:
                self.outputs.remove(socket)

    # Properterties edition on the node.
    def draw_buttons(self, context, layout):
        layout.label(text="Script:")
        layout.template_ID(self, "script", new="text.new", open="text.open")
        layout.prop(self, "work_group_size")

    # Properties interface on the sidebar.
    def draw_buttons_ext(self, context, layout):
        layout.label(text="Script:")
        layout.template_ID(self, "script", new="text.new", open="text.open")
        layout.operator("majax.compile_node_tree", text="Compile", icon="DISK_DRIVE")
        layout.prop(self, "work_group_size") # Use an str for python expr
        layout.label(text="")
        layout.label(text="Outputs")
        for out in self.outputs:
            if isinstance(out, MajaxSocketBuffers):
                row = layout.row()
                row.prop(out, "point_size")
                row.prop(out, "prim_size")