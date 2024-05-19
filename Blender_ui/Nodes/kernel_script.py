import bpy
from .base_node import BaseNode
from bpy.types import Node
from bpy.props import PointerProperty, IntProperty
from Blender_ui.Socket import MajaxSocketBuffers


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
        self.inputs.new("MajaxSocketBase", "")
        self.inputs[-1].intent = "in"
        self.outputs.new("MajaxSocketBase", "")
        self.outputs[-1].intent = "out"

    def update(self):
        """Executed when a new link is made. Delete Unconnected virtual socket"""
        # Delete or Create "inout" socket:
        for in_socket in self.inputs:
            if not in_socket.inout:
                continue
            if in_socket.out_id == -1:
                # Create the out socket if an in socket transform in inout socket (inverse case(out->inout) canno't happend)
                self.outputs.new(in_socket.bl_idname, in_socket.name)
                self.outputs[-1].inout = True # inout update --> reupdate the node !!! (before it's finished)
                new_socket_id = len(self.outputs)-1
                in_socket.out_id = new_socket_id-1 # -1 cz the move
                self.outputs.move(new_socket_id-1, new_socket_id)
            out_socket = self.outputs[in_socket.out_id]
            if not (in_socket.is_linked or out_socket.is_linked):
                # remove both sockets
                self.inputs.remove(in_socket)
                self.outputs.remove(out_socket)
                for in_socket in self.inputs: 
                    in_socket.recompute_out_id()

        # Delete "in" socket (could add with a move and a delete to automatically rewire on the new socket. then recreate a virtual socket)
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
        # Add "in" and "out" socket or made in the node_tree update

    # Properterties edition on the node.
    def draw_buttons(self, context, layout):
        layout.label(text="Script:")
        layout.template_ID(self, "script", new="text.new", open="text.open")
        layout.prop(self, "work_group_size", text="(expression or enum or both ??)")

    # Properties interface on the sidebar.
    def draw_buttons_ext(self, context, layout):
        layout.operator("mesh.primitive_monkey_add", text="Generate Sockets")
        layout.label(text="Script:")
        layout.template_ID(self, "script", new="text.new", open="text.open")
        layout.operator("majax.compile_node_tree", text="Compile", icon="DISK_DRIVE")
        layout.prop(self, "work_group_size") # Use an str for python expr
        layout.label(text="Inputs: ")
        for inp in self.inputs:
            if inp.bl_idname == "MajaxSocketBase": continue
            row = layout.row()
            row.label(text="    "+inp.name+": ")
            row.prop(inp, "inout", text="inout")
        layout.label(text="Outputs: ")
        for out in self.outputs:
            if out.bl_idname == "MajaxSocketBase" or out.intent=="inout": continue
            # layout.label(text=out.name+": ")
            row = layout.row()
            row.label(text="    "+out.name+": ")
            row.prop(out, "name")
            if isinstance(out, MajaxSocketBuffers):
                row = layout.row()
                row.prop(out, "point_size")
                row.prop(out, "prim_size")