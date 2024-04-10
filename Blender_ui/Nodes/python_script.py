# Une node qui permet d'écrire des Scrupt pythons
# Après avoir un Kernel qui fonction, 
# je vais essayer de copier un max le workflow OpenCL pour avoir une cohérance

import bpy
from .base_node import BaseNode
from bpy.types import Node
from bpy.props import EnumProperty, PointerProperty, IntProperty
from bpy.types import NodeSocketVirtual


class PythonScriptNode(BaseNode, Node):
    '''Execute the choosen python script'''
    # Optional identifier string.
    bl_idname = 'PythonScriptNode'
    # Label for nice name display
    bl_label = "Python Script"
    # Operator name id
    operator = "BlPythonScriptOperator"


    # === Properties ===
    script: PointerProperty(type=bpy.types.Text)
    # work_group_size: IntProperty(default=256, min=0)
    # device: EnumProperty(items=available_devices)

    def init(self, context):
        self.name = self.bl_label.replace(" ", "_")
        self.inputs.new('NodeSocketVirtual', "")
        self.outputs.new('NodeSocketVirtual', "")

    def update(self):
        """Delete Unconnected virtual socket"""
        # Could also update socket, by reading the script.
        # delta_socket = len(self.outputs) - len(self.inputs) # -1 car i commence à 1
        for i, socket in enumerate(self.inputs):
            print(i, socket)
            if i>=len(self.inputs)-1:
                continue
            if not socket.is_linked:
                self.inputs.remove(socket)
        for i, socket in enumerate(self.outputs):
            print("output socket: ", i, socket)
            if i>=len(self.outputs)-1:
                continue
            if not socket.is_linked:
                self.outputs.remove(socket)

    # Properterties edition on the node.
    def draw_buttons(self, context, layout):
        layout.label(text="Script:")
        layout.template_ID(self, "script", new="text.new", open="text.open")

    # Properties interface on the sidebar.
    def draw_buttons_ext(self, context, layout):
        layout.label(text="Script:")
        layout.template_ID(self, "script", new="text.new", open="text.open")