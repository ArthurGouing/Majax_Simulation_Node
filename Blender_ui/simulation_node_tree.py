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

        # Dynamic socket creation for VirtualSocketNode
        for i in self.links:
            if not (i.to_socket.bl_rna.name == i.from_socket.bl_rna.name):
                # Create Input socket if connected to Virtual Socket
                if (i.to_socket.bl_rna.name == "Virtual Node Socket"):
                    node = i.to_node

                    # new_socket_to = node.inputs.new(i.from_socket.bl_idname, i.from_socket.name) # replace bl_label by name ?? we can have name or type, don't which one is better
                    new_socket_to = node.inputs.new(i.from_socket.bl_idname, i.from_socket.name) # replace bl_label by name ?? we can have name or type, don't which one is better
                    if node.bl_idname == "SimInputNode":
                        # Create the equivalent node in the output
                        if i.from_socket.bl_idname == "NodeSocketGeometry":
                            node.outputs.new("NodeSocketBuffers", i.from_socket.name + " Buffers") #for sim in/out
                        else:
                            node.outputs.new(i.from_socket.bl_idname, i.from_socket.bl_label) #for sim in/out
                        to_socket_id = len(node.outputs)-2
                        node.outputs.move(to_socket_id, to_socket_id+1)
                    self.links.new(i.from_socket, new_socket_to)
                    self.links.remove(i)

                    # If linked to virtual, must have last id 
                    to_socket_id = len(node.inputs)-2
                    node.inputs.move(to_socket_id, to_socket_id+1)
                elif (i.from_socket.bl_rna.name == "Virtual Node Socket"):
                    node = i.from_node

                    new_socket_from = node.outputs.new(i.to_socket.bl_idname, i.to_socket.bl_label)
                    socket_to = i.to_socket
                    self.links.remove(i)
                    self.links.new(new_socket_from, socket_to)

                    from_socket_id = len(node.outputs)-2
                    node.outputs.move(from_socket_id, from_socket_id+1)
            elif i.from_socket.bl_rna.name == "Virtual Node Socket":
                self.links.remove(i)

        # Update Computational Grap un supplément dans l'adaptateur
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
        print("Ops: ", *[(o.id_name, o.inputs) for o in self.calculator.ops.values()], sep="\n")

    def execute(self, start_frame: int, last_frame: int) -> None:
        """ Realise the computation of the nodetree """
        n_frame = last_frame - start_frame
        self.calculator.compute(n_frame)

    def compile(self) -> None:
        self.calculator.update_graph(self.nodes, self.links)
        self.calculator.compile()
        

