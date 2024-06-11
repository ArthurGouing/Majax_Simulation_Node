#############################################################
# Copyright (C) 2025 Arthur Gouinguenet - All Rights Reserved
# This file is part of Majax Simulation Node project which is
# delivered under GNU General Public Liscense.
# For any questions or requests related to the use of this work
# please contact me directly at arthur.gouinguenet@free.fr
#############################################################


#### Library Import ####
from mathutils import Color

#### Blender Import ####
import bpy
from bpy.types import Node
from bpy.props import PointerProperty, EnumProperty, StringProperty, BoolProperty

#### Intern File Import ####
from .base_node import BaseNode
from Blender_ui.Socket import MajaxSocketBuffers

# Enum item
work_size_method = [
                    ('POINT', "Buffer point size", "1D Grid which have the same size than the number of points of the first inout Geometry Buffers", 0),
                    ('PRIM', "Buffer primitive size", "1D Grid which have the same size than the number of primitives of the first inout Geometry Buffers", 1),
                    ('CUSTOM', "Custom", "Enter a python expression which return the grid size as tuple of size<=3. You can use 'point_size' to access the number of point in the 1st inout buffer and 'prim_size' for the number of primitives (Read the documentation for relevant example).", 2)
]



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
    work_group_size: EnumProperty(items=work_size_method, name="Kernel size", description="Choose the method used to determine the size of the computation grid.")
    work_group_expr: StringProperty(name="", default="(point_shape[0],)")
    wait: BoolProperty(name="Wait", default=False)
    from_file: BoolProperty(name="Read file", default=True)

    def init(self, context):
        # Set name and color
        self.name = self.bl_label.replace(" ", "_")
        self.use_custom_color = True
        self.color = Color((0.059, 0.082, 0.188))

        # Inputs
        self.inputs.new("MajaxSocketBase", "")
        self.inputs[-1].intent = "in"

        # Outputs
        self.outputs.new("MajaxSocketBase", "")
        self.outputs[-1].intent = "out"

    # Update Node when a link is modified or a node is added/deleted
    def update(self):
        """Executed when a new link is made. Delete Unconnected virtual socket"""
        # Delete or Create "inout" socket:
        for in_socket in self.inputs:
            if not in_socket.inout:
                continue
            # Add inout (out)
            if in_socket.out_id == -1:
                # Create the out socket if an in socket transform in inout socket (inverse case(out->inout) cannot happend)
                self.outputs.new(in_socket.bl_idname, in_socket.name)
                self.outputs[-1].inout = True 
                new_socket_id = len(self.outputs)-1
                in_socket.out_id = new_socket_id-1 # -1 cz the move
                self.outputs.move(new_socket_id-1, new_socket_id)
            # Delete inout (in and out)
            out_socket = self.outputs[in_socket.out_id]
            if not (in_socket.is_linked or out_socket.is_linked):
                # remove both sockets
                self.inputs.remove(in_socket)
                self.outputs.remove(out_socket)
                for in_socket in self.inputs: 
                    in_socket.recompute_out_id()

        # Delete "in" socket
        for socket in self.inputs:
            if not (socket.is_linked or socket.bl_idname=="MajaxSocketBase" or socket.inout):
                self.inputs.remove(socket)
        # Delete useless "out" socket
        for socket in self.outputs:
            if not (socket.is_linked or socket.bl_idname=="MajaxSocketBase" or socket.inout):
                self.outputs.remove(socket)
                for in_socket in self.inputs: 
                    in_socket.recompute_out_id()
        # Note:
        # "in" and "out" socket are Added in the node_tree update

    # Properterties edition on the node.
    def draw_buttons(self, context, layout):
        layout.label(text="Script:")
        layout.template_ID(self, "script", new="text.new", open="text.open")
        layout.prop(self, "work_group_size", text="Size")
        if self.work_group_size == 'CUSTOM':
            layout.prop(self, "work_group_expr")
        row = layout.row()
        row.prop(self, "from_file")
        row.prop(self, "wait")

    # Properties interface on the sidebar.
    def draw_buttons_ext(self, context, layout):
        layout.operator("mesh.primitive_monkey_add", text="Generate Sockets") # TODO: change for something else
        layout.label(text="Script:")
        layout.template_ID(self, "script", new="text.new", open="text.open")
        layout.operator("majax.compile_node_tree", text="Compile", icon="DISK_DRIVE")
        layout.prop(self, "work_group_size") # Use an str for python expr
        if self.work_group_size == 'CUSTOM':
            layout.prop(self, "work_group_expr")
        row = layout.row()
        row.prop(self, "from_file")
        row.prop(self, "wait")

        # All sockets param
        # Inputs
        layout.label(text="Inputs: ")
        for inp in self.inputs:
            if inp.bl_idname == "MajaxSocketBase": continue
            row = layout.row()
            row.label(text="    "+inp.name+": ")
            row.prop(inp, "inout", text="inout")
            row.prop(inp, "name")

        # Outputs
        layout.label(text="Outputs: ")
        for out in self.outputs:
            if out.bl_idname == "MajaxSocketBase" or out.intent=="inout": continue
            # layout.label(text=out.name+": ")
            row = layout.row()
            row.label(text="    "+out.name+": ")
            row.prop(out, "name")
            if isinstance(out, MajaxSocketBuffers):
                row = layout.row()
                row.prop(out, "expr_size")