from bpy.types import Node
from bpy.props import IntProperty, EnumProperty, StringProperty
import pyopencl as cl


from .base_node import BaseNode
from ..Socket.geometry_buffers import MajaxSocketBuffers 

# TODO: assert only 1 SimInput for device can exist in the nodegraph !!! (placer dans le nodegraph update ??)

def get_type(t: int) -> str:
    if t==2: return "CPU"
    elif t==4: return "GPU"
    else: return cl.device_type.to_string(t)
ctx = cl.create_some_context(interactive=False)
available_devices = [(d.name.upper()+"_"+d.vendor.upper().replace(" ", "_"), get_type(d.type)+"_"+d.name, f"Device {d.name} ({d.vendor}) of type |{get_type(d.type)}|", i) for i, d in enumerate(ctx.devices)]

print("available debice:", available_devices)

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
    siminput: StringProperty(name="sim_input", description="name of the Linked SimulationInputNode.")

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
        self.inputs.new("MajaxSocketBase", "")
        self.inputs[-1].intent = "in"

        self.outputs.new("MajaxSocketBase", "")
        self.outputs[-1].intent = "out"
    
    # Delete Unconnected virtual socket
    def update(self):
        pass

    # Properterties edition on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, "device")
        layout.prop(self, "frequency")

    # Detail buttons in the sidebar.
    # If this function is not defined, the draw_buttons function is used instead
    # Properterties edition on the node.
    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "device")
        layout.prop(self, "frequency")
        layout.separator()
        layout.label(text="Inputs: ")
        for inp in self.inputs:
            if inp.bl_idname == "MajaxSocketBase": continue
            row = layout.row()
            row.label(text="    "+inp.name+": ")
        layout.label(text="Outputs: ")
        for out in self.outputs:
            if out.bl_idname == "MajaxSocketBase" or out.intent=="inout": continue
            row = layout.row()
            row.label(text="    "+out.name+": ")