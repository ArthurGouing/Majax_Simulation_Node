

# Mix-in class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation.
class BaseNode:
    bl_width_default = 220

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == "CustomTreeType"