from bpy.types import Node, NodeFrame
from bpy.props import IntProperty
from .base_node import BaseNode
# TODO: assert only 1 SimInput can exist in the nodegraph !!! (placer dans le nodegraph update ??)
# 
from mathutils import Color


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
    substep: IntProperty(default=0, min=0)

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
        self.inputs.new("NodeSocketGeometry", "Geometry")
        self.inputs.new("NodeSocketVirtual", "")

        self.outputs.new("NodeSocketFloat", "Delta Time")
        self.outputs.new("NodeSocketBuffers", "Geometry Buffers")
        self.outputs.new("NodeSocketVirtual", "")
    
    # Delete Unconnected virtual socket
    def update(self):
        print("update node")
        delta_socket = len(self.outputs) - len(self.inputs) # -1 car i commence à 1
        print(delta_socket, "delta socket doit valoir 1")
        for i, socket in enumerate(self.inputs):
            print(i, socket)
            if i==0 or i>=len(self.inputs)-1:
                continue
            if not socket.is_linked:
                self.inputs.remove(socket)
                self.outputs.remove(self.outputs[i+delta_socket]) # +1 car il y a 1 inputs de plus que d'output


    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, "substep")

    # Properties interface on the sidebar.
    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "substep")