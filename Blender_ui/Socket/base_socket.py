# Define the base socket with extra members that I need for dynamic socket and inout data type#### Import Library ####
#### Import Blender Library ####
from bpy.types import Context, UILayout, Node
from bpy.types import NodeSocket
#### Import files ####
from bpy.props import StringProperty, BoolProperty, IntProperty

def update_inout(self, context):
    # Compute intent string
    if self.is_output:
        self.intent = 'inout' if self.inout else 'out'
    else:
        self.intent = 'inout' if self.inout else 'in'

    if self.is_output:
        return

    # Compute out_id  ## Useless, it is done at the creation ? no cz socket can change dynamically
    self.recompute_out_id()
    
    # Create new socket if user interact with inout box
    self.node.update()


class MajaxSocketBase(NodeSocket):
    """The base socket class for the Majax sockets he also work as a virtual socket for dynamic socket creations"""
    bl_idname = "MajaxSocketBase"
    bl_label = ""

    # ==== Properties ====
    intent: StringProperty(name="intent", description="type of the socket", default="")  # TODO: delete (cf data/argument build)
    inout: BoolProperty(name="is_intent", description="bool which is true if socket type is inout.", default=False, update=update_inout)
    out_id: IntProperty(name="out_id", description="The id of the outputs associate with the in value when the socket is inout.", default=-1)


    def draw(self, context: Context, layout: UILayout, node: Node, text: str):
        layout.label(text=text)

    # Socket color
    @classmethod
    def draw_color_simple(cls):
        # Grey
        return (0.215, 0.215, 0.215, 1.0)

    def recompute_out_id(self):
        if self.inout:
            for i, s in enumerate(self.node.outputs):
                if s.name==self.name:
                    self.out_id = i
                    self.node.outputs[self.out_id].inout = True
                    break
        elif self.out_id !=-1:
            self.node.outputs[self.out_id].inout = False
            self.out_id = -1
        else:
            # oud_id already == -1 so we have nothing to change (this case shouln't happend)
            # print("do nothing about out_id in update_inout")
            # TODO a proper msg error if needed (seems that there is lot of normal case where it happen...)
            pass
