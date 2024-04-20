from bpy.types import Node, NodeSocketVirtual
from bpy.props import IntProperty, FloatProperty, EnumProperty
from .base_node import BaseNode
# TODO: assert only 1 SimInput can exist in the nodegraph !!! (placer dans le nodegraph update ??)
# 
from mathutils import Color
import pyopencl as cl

# Make automatique construction of the enum_list from OpenCL device
def get_type(t: int) -> str:
    if t==2: return "CPU"
    elif t==4: return "GPU"
    else: return cl.device_type.to_string(t)
ctx = cl.create_some_context(interactive=False)
available_devices = [(d.name.upper()+"_"+d.vendor.upper().replace(" ", "_"), get_type(d.type)+"_"+d.name, f"Device {d.name} ({d.vendor}) of type |{get_type(d.type)}|", i) for i, d in enumerate(ctx.devices)]
print("Available_device:", available_devices)

class SimInputNode(BaseNode, Node):
    """
    Start the simulation loop. 
    First convert the CPU object to GPU manipulatable object for the computation. 
    The data of the 'Output Simulation' will be received at each timestep 
    and the nodes between the Input and Output will be executed again
    """
    # Optional identifier string.
    bl_idname = "SimInputNode"
    # Label for nice name display
    bl_label = "Simulation Input"
    # Operator name id
    operator = "BlSimInputOperator"

    # === Properties ===
    substep: IntProperty(default=1, min=1)
    fps: FloatProperty()
    device: EnumProperty(items=available_devices, name="Device") # Ca c'est dans le sim input plutot

    def init(self, context):
        # Available socket: [NodesSocketInt, NodesSocketColor, NodesSocketVector, NodesSocketFloat, NodesSocketBool]
        self.name = self.bl_label.replace(" ", "_")
        self.inputs.new("MajaxSocketGeometry", "Geometry")
        self.inputs[-1].intent = "inout"
        self.inputs.new("NodeSocketVirtual", "")

        self.outputs.new("MajaxSocketBuffers", "Geometry Buffers")
        self.outputs[-1].intent = "out"
        self.outputs.new("NodeSocketVirtual", "")
        self.fps = context.scene.render.fps
        print("self.fps")
    
    # Delete Unconnected virtual socket
    def update(self):
        # Update socket creation
        delta_socket = len(self.outputs) - len(self.inputs) # -1 car i commence à 1
        for i, socket in enumerate(self.inputs):
            if i==0 or i>=len(self.inputs)-1:
                continue
            if not socket.is_linked:
                self.inputs.remove(socket)
                self.outputs.remove(self.outputs[i+delta_socket]) # +1 car il y a 1 inputs de plus que d'output
        
        # Update socket name
        # for socket in self.inputs:
        #     if isinstance(socket, NodeSocketVirtual):
        #         continue
        #     if socket.intent=="inout" and socket.links:
        #         socket.name = socket.links[0].from_socket.name


    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, "device")
        layout.prop(self, "substep")

    # Properties interface on the sidebar.
    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "device")
        layout.prop(self, "substep")