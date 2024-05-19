#### Library import #### 
from itertools import zip_longest

from bpy.types import NodeTree, Node
from Simulation import ComputeManager
####from Simulation import ComputationGraph
from .Socket import MajaxSocketGeometry, MajaxSocketBuffers
from .Nodes import SimOutputNode, SimInputNode


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
        print("update node tree")
        # Get SimInputNode and SimOutpuNode
        nodes_in = self.get_sim_input()   # TODO: don't work with multiple sim_input
        nodes_out = self.get_sim_output() # TODO: don't work with multiple sim_output

        # link the 2 node
        for n_in, n_out in zip(nodes_in, nodes_out):
            if n_out.device==n_in.device: # idem
                n_in.simoutput = n_out.name
                n_out.siminput = n_in.name

        # Dynamic socket creation for Simulation Loop
        for i in self.links:
            if not (i.to_socket.bl_rna.name == i.from_socket.bl_rna.name):
                if i.to_socket.bl_idname == "MajaxSocketBase":
                    src_socket = i.from_socket
                    node = i.to_node
                    # op
                    new_socket = node.inputs.new(src_socket.bl_idname, src_socket.name)
                    new_socket.intent = "in"
                    if isinstance(new_socket.node, SimInputNode) or isinstance(new_socket.node, SimOutputNode):
                        new_socket.inout = True
                    to_socket_id = len(node.inputs)-1
                    node.inputs.move(to_socket_id-1, to_socket_id)
                    # Rewire node
                    self.links.new(src_socket, new_socket)
                    self.links.remove(i)
                elif i.from_socket.bl_idname == "MajaxSocketBase":
                    src_socket = i.to_socket
                    node = i.from_node
                    # op
                    new_socket = node.outputs.new(src_socket.bl_idname, src_socket.name)
                    new_socket.intent = "out"
                    if isinstance(new_socket.node, SimOutputNode):
                        new_socket.inout = True

                    to_socket_id = len(node.outputs)-1
                    node.outputs.move(to_socket_id-1, to_socket_id)
                    # Rewire node
                    self.links.new(src_socket, new_socket)
                    # self.links.new(new_socket, src_socket)
                    # self.links.remove(i)
                else:
                    print("not the same socket type: error have to be raise")
                    self.links.remove(i)
            # update data name recursively -> all node that use the data after the link i
            elif i.from_socket.name!=i.to_socket.name: 
                # Warn: recursive function
                pass
                # self.rename_socket(i.to_socket, i.from_socket.name)

        # Assure SimInput and SimOutput consistency
        for n_in, n_out in zip(nodes_in, nodes_out):
            self.update_sim_socket(n_in, n_out)
        
        # Assure dynamic nodes consistency
        # for node in self.nodes:
        #     node.update_dynamic_socket()


    ######## Dynamic socket utils method ########

    def rename_socket(self, socket, name):
        """ Recursive function that rename the inputs socket 'socket', the inout_out socket associate. Then rename all the sockets that are connected to it (on the output)"""
        # Condition to avoid useless recursive renaming
        if socket.name==name:
            return
        # find inout socket on outputs
        if socket.inout:
            if isinstance(socket.node, SimInputNode) and socket.bl_label=="Geometry":
                old_name = socket.name + " Buffers"
            elif isinstance(socket.node, SimOutputNode) and socket.bl_label=="Geometry Buffers":
                old_name = socket.name[:-8]
            else:
                old_name = socket.name
            inout_socket = socket.node.outputs[old_name]
            if isinstance(socket.node, SimInputNode):
                simoutput_node = self.get_node(socket.node.simoutput)
                output_in_socket = simoutput_node.inputs[old_name]
        # update linked node inputs
        socket.name = name
        # if isinstance(socket.node, SimInputNode):
        #     self.update()
        # update linked node outputs if intent=='inout'
        if socket.inout:
            if isinstance(socket.node, SimInputNode): # ne passe pas parle là, socket.inout doit être false
                inout_socket.name = name+" Buffers" if inout_socket.bl_label=="Geometry Buffers" else name
            elif isinstance(socket.node, SimOutputNode):
                inout_socket.name = name[:-8] if inout_socket.bl_label=="Geometry" else name
            else:
                inout_socket.name = name
            if inout_socket.is_linked:
                for l in inout_socket.links:
                    self.rename_socket(l.to_socket, inout_socket.name)
            if isinstance(socket.node, SimInputNode):
                self.rename_socket(output_in_socket, name + " Buffers") # TODO: if want to add inout, will have to add conditions

    def get_sim_output(self): # TODO: get the simoutput which correspond to the siminput (if several GPU loops)
        nodes: list[Node] = list()
        for node in self.nodes:
            if node.bl_idname == "SimOutputNode":
                nodes.append(node)
        return nodes
    def get_sim_input(self): # TODO: idem
        nodes: list[Node] = list()
        for node in self.nodes:
            if node.bl_idname == "SimInputNode":
                nodes.append(node)
        return nodes
    def get_node(self, name):
        for node in self.nodes:
            if node.name == name:
                return node

    def create_socket(self, socket, socket_container, base_name): # socket container is either node.inputs or node.outputs
        # Create new_socket
        new_socket_to = socket_container.new(socket.bl_idname, base_name) # replace bl_label by name ?? we can have name or type, don't which one is better
        # Move virtual socket and the new socket
        to_socket_id = len(socket_container)-2
        socket_container.move(to_socket_id, to_socket_id+1)

        return new_socket_to

    
    def update_sim_socket(self, node_in, node_out):
        """
        Don't work with only in and only out because of conflict in name convention between SimInput and SimOutput
        """
        # Findt the longest list of data
        len_inin = len(node_in.inputs[:-1])
        len_inout = len(node_in.outputs[node_in.delta_socket:-1])
        len_outin = len(node_out.inputs[:-1])
        len_outout = len(node_out.outputs[:-1])
        if max([len_inin, len_inout, len_outin, len_outout]) == len_inout:
            socket_container = node_in.outputs[node_in.delta_socket:-1]
        elif max([len_inin, len_outin, len_outout]) == len_inin:
            socket_container = node_in.inputs[:-1]
        elif len_outin >= len_outout:
            socket_container = node_out.inputs[:-1]
        else:
            socket_container = node_out.outputs[:-1]

        # loop on all data, and assure coherense between SimInput and SimOuput
        for socket in socket_container:
            # Check if data is in both nodes else create it (some test are useless as we now the intent, but it is easier to read)
            is_simin_in   = [s for s in node_in.inputs   if (s.name==socket.name or s.name==socket.name.replace(" Buffers", ""))] 
            is_simin_out  = [s for s in node_in.outputs  if (s.name.replace(" Buffers", "")==socket.name or s.name==socket.name)]
            is_simout_in  = [s for s in node_out.inputs  if (s.name.replace(" Buffers", "")==socket.name or s.name==socket.name)]
            is_simout_out = [s for s in node_out.outputs if (s.name==socket.name or s.name==socket.name.replace(" Buffers", ""))]
            if True: #socket.intent=="inout" or socket.intent=="in":
                if not is_simin_in: 
                    if isinstance(socket, MajaxSocketBuffers):
                        s = self.create_socket(MajaxSocketGeometry, node_in.inputs, socket.name)
                    else:
                        s = self.create_socket(socket, node_in.inputs, socket.name)
                    s.inout = True
                if not is_simin_out:
                    if isinstance(socket, MajaxSocketGeometry):
                        s = self.create_socket(MajaxSocketBuffers, node_in.outputs, socket.name+" Buffers")
                    else:
                        s = self.create_socket(socket, node_in.outputs, socket.name)
                    s.inout = False
            if True: # socket.intent=="inout" or socket.intent=="out":
                if not is_simout_in:
                    if isinstance(socket, MajaxSocketGeometry):
                        s = self.create_socket(MajaxSocketBuffers, node_out.inputs, socket.name+" Buffers")
                    else:
                        s = self.create_socket(socket, node_out.inputs, socket.name)
                    s.inout = True
                if not is_simout_out:
                    if isinstance(socket, MajaxSocketBuffers):
                        s = self.create_socket(MajaxSocketGeometry, node_out.outputs, socket.name)
                    else:
                        s = self.create_socket(socket, node_out.outputs, socket.name)
                    s.inout = True
            
            # Check if the socket are connected else delete
            if not all([is_simin_in, is_simin_out, is_simout_in, is_simout_out]): # i.e. newly created and the var is_linked isn't correctly updated
                continue
            all_socket_is_link = [is_simin_in[0].is_linked, is_simin_out[0].is_linked, is_simout_in[0].is_linked, is_simout_out[0].is_linked]
            if not any(all_socket_is_link):
                node_in.inputs.remove(is_simin_in[0])
                node_in.outputs.remove(is_simin_out[0])
                node_out.inputs.remove(is_simout_in[0])
                node_out.outputs.remove(is_simout_out[0])
                


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
        
        # Test graph class
        print("Args:", *self.calculator.args.keys(), sep="\n")
        print("Ops: ", *[(o.id_name, [i.id_name for i in o.inputs], [i.id_name for i in o.outputs]) for o in self.calculator.ops.values()], sep="\n")