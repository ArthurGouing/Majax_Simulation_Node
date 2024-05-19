#### Import Library ####
#### Import Blender Library ####
from bpy.types import Context, UILayout, Node
#### Import files ####
from bpy.props import StringProperty
from .base_socket import MajaxSocketBase


class MajaxSocketGeometry(MajaxSocketBase):
    """Geometry CPU socket type"""
    bl_idname = "MajaxSocketGeometry"
    bl_label = "Geometry"

    size_expr: StringProperty(name="size_expr", description="python expression which return an tuple (or int) for the size of the buffer. Can use the inputs args data to create the size of the new buffer")

    def draw(self, context: Context, layout: UILayout, node: Node, text: str):
        layout.label(text=text)

    # Socket color
    @classmethod
    def draw_color_simple(cls):
        # Green
        return (0.0, 0.836, 0.636, 1.0)


    def recompute_out_id(self): # Override Base socket function
        if self.node.bl_idname=="SimInputNode":
            test_name = self.name + " Buffers" # self.name = "<name>"
        elif self.node.bl_idname=="SimOutputNode":
            test_name = self.name[:-8]         # self.name = "<name> Buffers"
        else:
            test_name = self.name

        if self.inout:
            for i, s in enumerate(self.node.outputs):
                if s.name==test_name:
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
