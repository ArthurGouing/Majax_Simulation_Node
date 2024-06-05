#### import ####
from Simulation import Operator, Data, OpenCLQueue
from abc import ABC, abstractmethod
import re
import numpy as np

class ControlStructure(ABC):

    def __init__(self, name: str, parent: str) -> None:
        # Name
        self.id_name = name
        # Ordered list of operator to execute
        self.childs: list[Operator] = list()
        # List of operator that belong to the Control structure flow
        self.child_names: list[str] = list()
        # eventual name of the Control Structure that engloble self
        self.parent: str = parent

    def append_name(self, name: str) -> None:
        self.child_names.append(name)

    def append(self, op: Operator) -> None:
        self.childs.append(op)

    @abstractmethod
    def compute(self) -> None:
        pass


class BlControlStructureLoop(ControlStructure):
    def __init__(self, node) -> None:
        self.name = re.search("(.*) ite: \d*", node.label).group(1)
        self.ite = node.ite
        if node.parent:
            parent = node.parent.name
        else:
            parent = None
        super().__init__(node.name, parent)

    def compute(self,queue: OpenCLQueue, datas: dict[str, Data]) -> None:
        datas.update({self.name: PseudoData(np.int32(0))}) # TODO: Done at each subite. Create in in the read_graph like other datas
        for i in range(self.ite):
            for op in self.childs:
                datas[self.name].data = np.int32(i)
                op.compute(queue, datas)


class BlControlStructureCondition(ControlStructure):
    def __init__(self, node) -> None:
        self.is_first = True
        self.expr = node.expression
        if node.parent:
            parent = node.parent.name
        else:
            parent = None
        super().__init__(node.name, parent)

    def compute(self, queue: OpenCLQueue, datas: dict[str, Data]) -> None:
        if self.is_first:
            self.local = datas.copy() # TODO: check if it only copy ptr (in any case it impact memory not sim performance bcz exec 1 time --> neglectabe)
            self.is_first = False
        glob = {}
        exec("majax_exec = "+self.expr, glob, self.local)
        execute = self.local["majax_exec"]
        if execute:
            for op in self.childs:
                op.compute(queue, datas)

class PseudoData():
    def __init__(self, value: np.integer) -> None:
        self.data_type = "int"
        self.data = value
        pass