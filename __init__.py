# 
# 
# 
# 
# Add current dirctory to Python Path
import sys, os, importlib
sys.path.append(os.path.dirname(__file__))
os.environ["PYTHONPATH"] = os.path.dirname(__file__)
os.environ["PYOPENCL_COMPILER_OUTPUT"] = "1"

# Utils
import bpy
from bpy.utils import register_class, unregister_class
from time import perf_counter

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
        "INPUTS",
        "Inputs Datas",
        items=[
            NodeItem("ImportGeoNode"),
            NodeItem("FloatParameterNode"),
            NodeItem("VectorParameterNode"),
            NodeItem("IntegerParameterNode"),
            NodeItem("TransformCombineNode"),
        ]
    ),
    MajaxNodeCategory(
        "OUTPUTS",
        "Outputs Datas",
        items=[
            NodeItem("ExportGeoNode")
        ]
    ),
    MajaxNodeCategory(
        "GPU",
        "Simulation Operators (GPU)",
        items=[
            NodeItem("SimInputNode"),
            NodeItem("SimOutputNode"),
            NodeItem("KernelScriptNode"),
            NodeItem("KernelCopyNode"),
            NodeItem("KernelTestNode"),
        ],
    ),
    MajaxNodeCategory(
        "CPU",
        "Post/Pre Processing Operators (CPU)",
        items=[
            NodeItem("PythonScriptNode")
        ],
    ),
]

# Handlers function
def stop_playback(scene):
    if(scene.frame_current == scene.frame_end):
        bpy.ops.screen.animation_cancel(restore_frame=False)

def step_forward(scene):
    """ 
    Rules of computation according to frame change:
     - if we go to the next frame:     Compute one Simulation loop
     - if we go to the previous frame: Do nothing
     - if we jump to a father frame:   Reset the computation
     - if we compile and go to the next step: the computation is'nt init --> Faire l'init dans la compile ?
    """
    t_start=perf_counter()
    if not scene.majax_node_tree: # idem
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

    ### Add scene property ###
    bpy.types.Scene.majax_node_tree = bpy.props.PointerProperty(type=bpy.types.NodeTree, name="majax_node")
    bpy.types.Scene.frame_previous = bpy.props.IntProperty(name="p_frame", default=0)

    ### Add other property ### 
    bpy.types.NodeSocketVirtual.intent = bpy.props.StringProperty(name="intent")

    ### Add handlers
    # bpy.app.handlers.animation_playback_pre.append(pre_process)
    bpy.app.handlers.frame_change_pre.append(step_forward)
    #TODO: Pas indispensable mais je ferais un parametre à coté du Run/Compile pour Loop ou pas la Timeline
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
    del bpy.types.NodeSocketVirtual.intent

    ### Remove handlers
    # bpy.app.handlers.animation_playback_pre.remove(pre_process)
    try:
        bpy.app.handlers.frame_change_pre.remove(bpy.app.handlers.frame_change_pre[0])   # WARN: may cause conflict with other add-on
        # bpy.app.handlers.frame_change_post.remove(bpy.app.handlers.frame_change_post[0]) # idem
    except:
        pass
