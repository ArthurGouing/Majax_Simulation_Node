#############################################################
# Copyright (C) 2025 Arthur Gouinguenet - All Rights Reserved
# Majax is a Blender Add-on which allow GPU computation
# for simulation into Blender. Majax is delivered under
# GNU General Public Liscense.
#
# This license grants you a number of freedoms:
#   * You are free to use it, for any purpose
#   * You are free to distribute it
#   * You can study how Majax works and change it
#   * You can distribute changed versions of Majax.
# The GPL strictly aims at protecting these freedoms,
# requiring everyone to share their modifications when they
# also share the software in public. Please be advised that
# you are not allowed to owning, registering copyright and
# earning royalties from copyright.
#
# By using or distributing this work, you agree to respect
# these moral rights and acknowledge that any violation of
# these rights may result in legal action. For any questions
# or requests related to the use of this work, please
# contact me directly at arthur.gouinguenet@free.fr
#
#############################################################
#### Library Import ####
import sys, os, re
from time import perf_counter

#### Blender Import #### 
import bpy
from bpy.utils import register_class, unregister_class

#### Local Import ####
import Blender_ui



# Set global variables
sys.path.append(os.path.dirname(__file__))
os.environ["PYTHONPATH"] = os.path.dirname(__file__)
os.environ["PYOPENCL_COMPILER_OUTPUT"] = "1"

ui_class_list = Blender_ui.__all__


# Addon informations
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

frame_type = [
    ("NOTE", "Note", "Do not have any impact on the node, act like a classical frame", 0),
    ("LOOP", "Repeat", "Repeat the inner kernels (act like a for loop)", 1),
    ("IF", "Condition", "Execute the inner kernels if the condition is respected (act like a if)", 2),
]


def update_ite(self, context):
    r = re.findall("(.*) (ite: \d*)", self.label)
    if r:
        self.label = r[0][0] + " ite: " + str(self.ite)
    else:
        self.label = self.label + " ite: " + str(self.ite)


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
        "INPUTS",
        "Inputs Datas",
        items=[
            NodeItem("ImportGeoNode"),
            NodeItem("FloatParameterNode"),
            NodeItem("VectorParameterNode"),
            NodeItem("IntegerParameterNode"),
            NodeItem("TransformCombineNode"),
        ],
    ),
    MajaxNodeCategory("OUTPUTS", "Outputs Datas", items=[NodeItem("ExportGeoNode")]),
    MajaxNodeCategory(
        "GPU",
        "Simulation Operators (GPU)",
        items=[
            NodeItem("SimInputNode"),
            NodeItem("SimOutputNode"),
            NodeItem("KernelScriptNode"),
            NodeItem("KernelCopyNode"),
            NodeItem("KernelTestNode"),
            NodeItem(
                "NodeFrame", label="Repeat", settings={"operator": repr("LOOP"), "label": repr("Repeat")}
            ),
            NodeItem(
                "NodeFrame",
                label="Condition",
                settings={"operator": repr("IF"), "label": repr("Condition")},
            ),
        ],
    ),
    MajaxNodeCategory(
        "CPU",
        "Post/Pre Processing Operators (CPU)",
        items=[
            NodeItem("PythonScriptNode"),
            NodeItem(
                "NodeFrame", label="Repeat", settings={"operator": repr("LOOP"), "label": repr("Repeat")}
            ),
            NodeItem(
                "NodeFrame",
                label="Condition",
                settings={"operator": repr("IF"), "label": repr("Condition")},
            ),
        ],
    ),
]

# classes = (SimulationNodeTree, MyCustomSocket, MyCustomInterfaceSocket, MyCustomNode, SimInputNode)
print("\nLodaing Blender classes:")
print(*ui_class_list, sep="  |  ")
print("")
classes = [Blender_ui.__dict__[class_name] for class_name in ui_class_list]
# custom_classes = [Simulation.__dict__[class_name] for class_name in sim_class_list]


# Handlers function
def stop_playback(scene):
    if scene.frame_current == scene.frame_end:
        bpy.ops.screen.animation_cancel(restore_frame=False)


def step_forward(scene):
    """
    Rules of computation according to frame change:
     - if we go to the next frame:     Compute one Simulation loop
     - if we go to the previous frame: Do nothing
     - if we jump to a father frame:   Reset the computation
     - if we compile and go to the next step: the computation is'nt init --> Faire l'init dans la compile ?
    """
    t_start = perf_counter()
    if not scene.majax_node_tree:  # idem
        return
    # Decide if computation have to be refresh:
    delta_frame = scene.frame_current - scene.frame_previous
    # update previous frame
    scene.frame_previous = scene.frame_current
    # Compute
    print("delta frame:", delta_frame)
    if delta_frame == 1:
        # Compute one Simulation Loop and one post-process
        t_1 = perf_counter()
        if not hasattr(scene.majax_node_tree, "calculator"):
            scene.majax_node_tree.compile()
        elif scene.majax_node_tree.need_init:
            scene.majax_node_tree.init_compute()
        t_2 = perf_counter()
        scene.majax_node_tree.step_forward()
        t_3 = perf_counter()
        scene.majax_node_tree.update_computed_data()
        t_4 = perf_counter()
    elif delta_frame != -1 and delta_frame != 0:
        # Do the pre-process part and reset  GPU buffers
        if not hasattr(scene.majax_node_tree, "calculator"):
            scene.majax_node_tree.compile()
        scene.majax_node_tree.init_compute()
        scene.majax_node_tree.update_computed_data()
    t_end = perf_counter()
    print(f"\nFrame {scene.frame_current}  time: {(t_end-t_start)*1000:.3f} ms ({t_end-t_start:f} s)")
    try:
        print(f"Detail:")
        print(f"  if:           {(t_2-t_1)*1000}")
        print(f"  step_forward: {(t_3-t_2)*1000}")
        print(f"  update_data:  {(t_4-t_3)*1000}")
        print(f"  else:         {(t_end-t_4)*1000}")
    except:
        pass
    print("")


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

    ### Add scene property ###
    bpy.types.Scene.majax_node_tree = bpy.props.PointerProperty(
        type=bpy.types.NodeTree, name="majax_node"
    )
    bpy.types.Scene.frame_previous = bpy.props.IntProperty(name="p_frame", default=0)

    ### Add other property ###
    bpy.types.NodeFrame.operator = bpy.props.EnumProperty(
        items=frame_type,
        name="Operator",
        description="Logical Operator to be executed on the inner operators",
    )
    bpy.types.NodeFrame.ite = bpy.props.IntProperty(
        name="Iterations",
        description="Number of type to repeate the inner operators",
        default=0,
        update=update_ite,
    )
    bpy.types.NodeFrame.expression = bpy.props.StringProperty(
        name="", description="Expression needed for the frame operator", default=""
    )
    # bpy.types.NodeSocketVirtual.intent = bpy.props.StringProperty(name="intent")

    ### Add handlers
    # bpy.app.handlers.animation_playback_pre.append(pre_process)
    bpy.app.handlers.frame_change_pre.append(step_forward)
    # TODO: Pas indispensable mais je ferais un parametre à coté du Run/Compile pour Loop ou pas la Timeline
    # bpy.app.handlers.frame_change_post.append(stop_playback)


def unregister():
    print("Unregister classes")
    nodeitems_utils.unregister_node_categories("CUSTOM_NODES")

    for cls in reversed(classes):
        print(cls.__name__, cls)
        unregister_class(cls)

    ### Remove scene property
    del bpy.types.Scene.majax_node_tree
    del bpy.types.Scene.frame_previous
    del bpy.types.NodeFrame.operator
    del bpy.types.NodeFrame.ite
    del bpy.types.NodeFrame.expression
    # del bpy.types.NodeSocketVirtual.intent

    ### Remove handlers
    # bpy.app.handlers.animation_playback_pre.remove(pre_process)
    try:
        bpy.app.handlers.frame_change_pre.remove(
            bpy.app.handlers.frame_change_pre[0]
        )  # WARN: may cause conflict with other add-on
        # bpy.app.handlers.frame_change_post.remove(bpy.app.handlers.frame_change_post[0]) # idem
    except:
        pass
