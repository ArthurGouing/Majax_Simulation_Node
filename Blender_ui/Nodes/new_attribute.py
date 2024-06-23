#############################################################
# Copyright (C) 2025 Arthur Gouinguenet - All Rights Reserved
# This file is part of Majax Simulation Node project which is
# delivered under GNU General Public Liscense.
# For any questions or requests related to the use of this work
# please contact me directly at arthur.gouinguenet@free.fr
#############################################################


#### Library Import ####
from mathutils import Color

#### Blender Import ####
from bpy.types import Node
from bpy.props import StringProperty, EnumProperty, BoolProperty

#### Intern File Import ####
from .base_node import BaseNode

# Enum Items
variable_type = [
    ("FLOAT", "Float", "A 32bits float at the 0 value", 0),
    ("INT", "Integer", "Create a null integer", 2),
    ("VECTOR", "Vector", "Create 4 float array, init at 0", 3),
    ("ROTATION", "Rotation Matrix", "Create a 3x3 matrix, init at 0", 4),
    ("TRANSFORMATION", "Transformation", "Create a 4x4 matrix, init at 0", 5),
]
elem_type = [
    ("POINT", "Point", "Have a different value for each point of the geometry", 0),
    ("PRIM", "Primitive", "Have a difference value for each primitive of the geometry", 1),
]


class CreateAttributeNode(BaseNode, Node):
    """Create a new empty attribute to the geometry"""

    # Identifier string.
    bl_idname = "CreateAttributeNode"
    # Label for nice name display
    bl_label = "Create empty attribute"
    # Executor name
    operator = "BlCreateAttributeOperator"

    # === Properties ===
    var_name: StringProperty(name="Name", description="Name of the geometry variable")
    var_type: EnumProperty(
        items=variable_type, name="Type", description="Choose the type of the new attribute"
    )
    is_uniform: BoolProperty(
        name="Uniform",
        description="Can have a different value for each element of the Geometry",
        default=True,
    )
    is_stationary: BoolProperty(
        name="Stationary",
        description="If the attribute is stationnary, the value of the attribute won't change during the simulation, and wouldn't be update on the CPU to optimize the performance",
        default=True,
    )
    element_type: EnumProperty(
        items=elem_type, name="", description="Choose between point elements or primitive elements"
    )
    is_vec: BoolProperty(name="Is vector", description="Can have multiple value for each elements")
    size: StringProperty(name="Size", description="Size of the vecteur field")
    use_double: BoolProperty(name="Use double", description="To use float64 in the numpy arrays. (Currently not supported on Kernels)")
    is_local_memory: BoolProperty(name="Use Local Memory", description="Must be True to use the buffer as a local memomry in the OpenCL Kernels.")

    def init(self, context):
        # Set name and color
        self.name = self.bl_label.replace(" ", "_")
        self.use_custom_color = True
        self.color = Color((0.056, 0.188, 0.155))

        # Inputs
        self.inputs.new("MajaxSocketGeometry", "Geometry")
        self.inputs[-1].intent = "inout"

        # Outputs
        self.outputs.new("MajaxSocketGeometry", "Geometry")
        self.outputs[-1].intent = "inout"

    # Update Node when a link is modified or a node is added/deleted
    def update(self):
        pass

    # Properterties edition on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, "var_type")
        layout.prop(self, "var_name")
        row = layout.row()
        row.prop(self, "is_uniform")
        if not self.is_uniform:
            row.prop(self, "element_type")
        layout.prop(self, "is_stationary")
        row = layout.row()
        row.prop(self, "is_vec")
        if self.is_vec:
            row.prop(self, "size")
        layout.prop(self, "use_double")
        layout.prop(self, "is_local_memory")

    # Properties interface on the sidebar.
    def draw_buttons_ext(self, context, layout):
        layout.prop(self.inputs[0], "name", text="Socket Name")
        layout.separator()
        layout.prop(self, "var_type")
        layout.prop(self, "var_name", text="Var name")
        row = layout.row()
        row.prop(self, "is_uniform")
        if not self.is_uniform:
            row.prop(self, "element_type")
        layout.prop(self, "is_stationary")
        row = layout.row()
        row.prop(self, "is_vec")
        if self.is_vec:
            row.prop(self, "size")
        layout.prop(self, "use_double")
        layout.prop(self, "is_local_memory")
