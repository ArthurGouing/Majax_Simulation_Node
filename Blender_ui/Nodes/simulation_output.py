from bpy.types import Node
from bpy.props import IntProperty, EnumProperty
import pyopencl as cl


from .base_node import BaseNode

# TODO: assert only 1 SimInput for device can exist in the nodegraph !!! (placer dans le nodegraph update ??)

def get_type(t: int) -> str:
    if t==2: return "CPU"
    elif t==4: return "GPU"
    else: return cl.device_type.to_string(t)
ctx = cl.create_some_context(interactive=False)
available_devices = [(d.name.upper()+"_"+d.vendor.upper().replace(" ", "_"), get_type(d.type)+"_"+d.name, f"Device {d.name} ({d.vendor}) of type |{get_type(d.type)}|", i) for i, d in enumerate(ctx.devices)]

class SimOutputNode(BaseNode, Node):
    """
    End the simulation loop. 
    Send GPU data to CPU to print the data to the viewport
    Send the data of the 'Input Simulation' at each timestep
    The data of the 'Output Simulation' will be received at each timestep 
    and the nodes between the Input and Output will be executed again
    """
    # Optional identifier string.
    bl_idname = "SimOutputNode"
    # Label for nice name display
    bl_label = "Simulation Output"
    # Operator name id
    operator = "BlSimOutputOperator"

    # === Properties ===
    frequency: IntProperty(default=1, min=1)
    device: EnumProperty(items=available_devices, name="Device") # Ca c'est dans le sim input plutot

    def init(self, context):
        # Available socket: [NodesSocketInt, NodesSocketColor, NodesSocketVector, NodesSocketFloat, NodesSocketBool]
        # self.inputs.new("NodeSocketColor", "test")
        # self.inputs.new("NodeSocketFloat", "test")
        # self.inputs.new("NodeSocketInt", "test")
        # self.inputs.new("NodeSocketStandard", "test")
        # self.inputs.new("NodeSocketMaterial", "test")
        # self.inputs.new("NodeSocketShader", "test")
        # self.inputs.new("NodeSocketVector", "test")
        # self.inputs.new("NodeSocketImage", "test")
        # self.inputs.new("NodeSocketObject", "GPU_buffer")
        self.name = self.bl_label.replace(" ", "_")
        self.inputs.new("MajaxSocketBuffers", "Geometry Buffers")
        self.inputs[-1].intent = "in"
        self.inputs.new("NodeSocketVirtual", "")

        self.outputs.new("MajaxSocketGeometry", "Geometry")
        self.outputs[-1].intent = "inout"
        self.outputs.new("NodeSocketVirtual", "")
    
    # Delete Unconnected virtual socket
    def update(self):
        delta_socket = len(self.outputs) - len(self.inputs) # -1 car i commence à 1
        for i, socket in enumerate(self.inputs):
            if i==0 or i>=len(self.inputs)-1:
                continue
            if not socket.is_linked:
                self.inputs.remove(socket)
                self.outputs.remove(self.outputs[i+delta_socket]) # +1 car il y a 1 inputs de plus que d'output

    # Properterties edition on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, "device")
        layout.prop(self, "frequency")
        pass

    # Detail buttons in the sidebar.
    # If this function is not defined, the draw_buttons function is used instead
    # Properterties edition on the node.
    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "device")
        layout.prop(self, "frequency")