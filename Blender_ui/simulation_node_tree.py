from bpy.types import NodeTree
from Simulation import ComputeManager
####from Simulation import ComputationGraph


# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class SimulationNodeTree(NodeTree):  # Target
    # Description string
    """Simulation node, that manage all the Majax Node workspace"""
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = "CustomTreeType"
    # Label for nice name display
    bl_label = "Majax Node Editor"
    # Icon identifier
    bl_icon = "MEMORY" # NETWORK_DRIVE or PHYSICS could also be a good choice

    def __init__(self) -> None:
        """ This function will be never executed for some reson. The calculator is created in an try/except statement"""
        print("Init SimulationNodeTree !!!")
        super().__init__()
        self.calculator = ComputeManager()

    def update(self):
        """
        Executed when a change happen in the graph. Check forbiden link 
        and add virtual link for multiple inputs/output nodes
        """
        # Find Simulation Input and Output and link them
        # En espérant que 2 loops on node ne soit pas trop... Il suffit de le faire/try 1 fois à l'init !
        for in_node in self.nodes:
            if not hasattr(in_node, "device"):
                continue
            if in_node.bl_idname=="SimInputNode":
                for out_node in self.nodes:
                    if not hasattr(out_node, "device"):
                        continue
                    if out_node.bl_idname=="SimOutputNode" and out_node.device==in_node.device:
                        in_node.simoutput = out_node.name
                        out_node.siminput = in_node.name

        # Dynamic socket creation for Simulation Loop
        for i in self.links:
            if not (i.to_socket.bl_rna.name == i.from_socket.bl_rna.name): # not the same socket type
                # Create Input socket if connected to Virtual Socket
                if (i.to_socket.bl_idname == "NodeSocketVirtual"):
                    node = i.to_node
                    socket_src = i.from_socket
                    self.create_input_socket(socket_src, node)
                    self.links.remove(i)
                    if node.bl_idname == "SimInputNode":
                        sim_output_node = self.get_sim_output()
                        self.create_output_socket(socket_src, sim_output_node)
                # Create Output socket if connected to Virtual Socket
                elif (i.from_socket.bl_idname == "NodeSocketVirtual"):
                    node = i.from_node
                    socket_src = i.to_socket
                    self.create_output_socket(socket_src, node)
                    self.links.remove(i)
                    if node.bl_idname == "SimOutputNode":
                        sim_input_node = self.get_sim_input()
                        self.create_input_socket(socket_src, sim_input_node)
            # Delete link between 2 virtual sockets
            elif i.from_socket.bl_idname == "NodeSocketVirtual":
                self.links.remove(i)

        # Delete unused dynamic socket for SimInput and SimOutput (can't do in node update cz thoses 2 nodes sockets depend on each others)
        # ...
        # Todo
        # ...

        # Update Computational Graph
        try:
            self.calculator.update_graph(self.nodes, self.links)
        except AttributeError:
            self.calculator = ComputeManager()
            self.calculator.update_graph(self.nodes, self.links)
        except Exception as e:
            raise e

        # Test graph class
        # args = graph.get_args()
        print("Args:", *self.calculator.args.keys(), sep="\n")
        # ops = graph.get_ops()
        print("Ops: ", *[(o.id_name, [i.id_name for i in o.inputs], [i.id_name for i in o.outputs]) for o in self.calculator.ops.values()], sep="\n")



    ######## Dynamic socket utils method ########

    def get_sim_output(self):
        for node in self.nodes:
            if node.bl_idname == "SimOutputNode":
                return node
    def get_sim_input(self):
        for node in self.nodes:
            if node.bl_idname == "SimInputNode":
                return node

    def create_input_socket(self, socket, node):
        n = len([s for s in node.inputs if s.bl_idname==socket.bl_idname])
        name = socket.from_socket.bl_label if n==0 else socket.bl_label+" "+str(n)
        new_socket_to = node.inputs.new(socket.bl_idname, name) # replace bl_label by name ?? we can have name or type, don't which one is better
        if node.bl_idname == "SimInputNode":
            # Create the equivalent node in the output
            if socket.bl_idname == "MajaxSocketGeometry":
                node.outputs.new("MajaxSocketBuffers", "Geometry Buffers "+ str(n)) #for sim in/out
            else:
                node.outputs.new(socket.bl_idname, name) #for sim in/out
            to_socket_id = len(node.outputs)-2
            node.outputs.move(to_socket_id, to_socket_id+1)
        self.links.new(socket, new_socket_to)
        # If linked to virtual, must have last id 
        to_socket_id = len(node.inputs)-2
        node.inputs.move(to_socket_id, to_socket_id+1)

    def create_output_socket(self, socket, node):
        n = len([s for s in node.outputs if s.bl_idname==socket.bl_idname])
        name = socket.bl_label if n==0 else socket.bl_label+" "+str(n)
        new_socket_from = node.outputs.new(socket.bl_idname, name)
        if node.bl_idname == "SimOutputNode":
            # Create the equivalent node in the input
            if socket.bl_idname == "MajaxSocketGeometry":
                node.inputs.new("MajaxSocketBuffers", "Geometry Buffers"+ str(n)) #for sim in/out
            else:
                node.inputs.new(socket.bl_idname, name) #for sim in/out
            to_socket_id = len(node.inputs)-2
            node.inputs.move(to_socket_id, to_socket_id+1)
        socket_to = socket
        self.links.new(new_socket_from, socket_to)

        from_socket_id = len(node.outputs)-2
        node.outputs.move(from_socket_id, from_socket_id+1)


    ######## Computation related method ########

    def init_compute(self):
        self.calculator.init_compute()

    def step_forward(self):
        self.calculator.step_forward()

    def update_computed_data(self):
        self.calculator.update_computed_data()

    def execute(self, start_frame: int, last_frame: int) -> None:
        """ Realise the computation of the nodetree """
        n_frame = last_frame - start_frame
        self.calculator.compute(n_frame)

    def compile(self) -> None:
        try:
            self.calculator.update_graph(self.nodes, self.links)
        except AttributeError:
            self.calculator = ComputeManager()
            self.calculator.update_graph(self.nodes, self.links)
        except Exception as e:
            raise e
        self.calculator.compile()
        

