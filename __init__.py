# 
# 
# 
# 
# Add current dirctory to Python Path
import sys, os, importlib
sys.path.append(os.path.dirname(__file__))
os.environ["PYTHONPATH"] = os.path.dirname(__file__)

# Utils
import bpy
from bpy.utils import register_class, unregister_class

# Import Addon files
# Overwrite 
import Blender_ui
# import Simulation

# Load the list of class used by the add-on
# sim_class_list = Simulation.__all__
ui_class_list = Blender_ui.__all__

bl_info = {
    "name": "Majax Node",
    "author": "Arthos",
    "description": "Provide a node interface to develop simulation computation with OpenCL",
    "blender": (4, 1, 0),
    "version": (0, 0, 1),
    "location": "Majax Node",
    "warning": "",
    "category": "Physics",
}

### Node Categories ###
# Node categories are a python system for automatically
# extending the Add menu, toolbar panels and search operator.
# For more examples see scripts/startup/nodeitems_builtins.py

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

# our own base class with an appropriate poll function,
# so the categories only show up in our own tree type


class MajaxNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "CustomTreeType"


# all categories in a list
node_categories = [
    MajaxNodeCategory(
        "SIMULATION_UTILS",
        "Tools",
        items=[
            NodeItem("ImportGeoNode"),
            NodeItem("ExportGeoNode"),
            NodeItem("SimInputNode"),
            NodeItem("SimOutputNode"),
            NodeItem("KernelScriptNode"),
            NodeItem("KernelTestNode"),
            NodeItem("PythonScriptNode")
        ],
    ),
    MajaxNodeCategory(
        "OTHERNODES",
        "Other Nodes",
        items=[
            # the node item can have additional settings,
            # which are applied to new nodes
            # NOTE: settings values are stored as string expressions,
            # for this reason they should be converted to strings using repr()
            NodeItem(
                "SimInputNode",
                label="Node A",
                settings={
                    "my_string_prop": repr("Lorem ipsum dolor sit amet"),
                    "my_float_prop": repr(1.0),
                },
            ),
            NodeItem(
                "SimOutputNode",
                label="Node B",
                settings={
                    "my_string_prop": repr("consectetur adipisicing elit"),
                    "my_float_prop": repr(2.0),
                },
            ),
        ],
    ),
]

# classes = (SimulationNodeTree, MyCustomSocket, MyCustomInterfaceSocket, MyCustomNode, SimInputNode)
print("\nLodaing Blender classes:")
print(*ui_class_list, sep="  |  ")
print("")
classes  = [Blender_ui.__dict__[class_name] for class_name in ui_class_list]
# custom_classes = [Simulation.__dict__[class_name] for class_name in sim_class_list]



def register():
    print("Register classes")
    ### ADD Context Properties ### 
    # bpy.types.ToolSettings.restart = bpy.props.BoolProperty(name="test property") # , description="Go to start frame when running the node graph", default=True)
    ### Register Class ###  
    for cls in classes:
        print("register: ", cls.__name__)
        register_class(cls)

    ### Register node add menu ### 
    nodeitems_utils.register_node_categories("CUSTOM_NODES", node_categories)


def unregister():
    print("Unregister classes")
    nodeitems_utils.unregister_node_categories("CUSTOM_NODES")

    for cls in reversed(classes):
        unregister_class(cls)
