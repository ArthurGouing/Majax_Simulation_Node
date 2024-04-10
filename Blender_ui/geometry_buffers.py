from bpy.types import NodeSocket, NodeTreeInterfaceSocket
from bpy.props import FloatProperty

# Custom socket type
class NodeSocketBuffers(NodeSocket):
    # Description string
    """Geometry GPU buffer socket type"""
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = "NodeSocketBuffers"
    # Label for nice name display
    bl_label = "Geometry Buffers"
    # Can handl multiple inputs
    # display_shape = 'DIAMOND_DOT'
    # display_shape = 'DIAMOND'
    # display_shape = 'SQUARE_DOT'
    display_shape = 'SQUARE'

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        layout.label(text=text)

    # Socket color
    @classmethod
    def draw_color_simple(cls):
        # Blue
        return (0.0, 0.117, 0.672, 1.0)

# Customizable interface properties to generate a socket from.
class NodeTreeInterfaceSocketBuffers(NodeTreeInterfaceSocket):
    # The type of socket that is generated.
    bl_socket_idname = "GeometryBuffersType"

    def draw(self, context, layout):
        # Display properties of the interface.
        layout.label("Test")

    # Set properties of newly created sockets
    def init_socket(self, node, socket, data_path):
        # socket.input_value = self.default_value
        pass

    # Use an existing socket to initialize the group interface
    def from_socket(self, node, socket):
        # Current value of the socket becomes the default
        # self.default_value = socket.input_value
        pass