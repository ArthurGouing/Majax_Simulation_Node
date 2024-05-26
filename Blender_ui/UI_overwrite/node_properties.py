from bpy.types import Panel

class NODE_PT_active_node_properties(Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Node"
    bl_label = "Properties"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.active_node is not None

    def draw(self, context):
        layout = self.layout
        node = context.active_node
        layout.template_node_inputs(node)
        if node.type=='FRAME':
            layout.prop(node, "operator")
            if node.operator=='LOOP':
                layout.prop(node, "ite")
            elif node.operator=='IF':
                layout.prop(node, "expression")
