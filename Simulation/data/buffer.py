#################################################
# Copyright (C) 2025 Arthur Gouinguenet - All Rights Reserved
# This file is part of Majax Simulation Node project which is
# delivered under GNU General Public Liscense.
# For any questions or requests related to the use of this work
# please contact me directly at arthur.gouinguenet@free.fr
#############################################################

#### Library Import ####
import numpy as np
import pyopencl as cl

#### Local Import #### 
from Simulation.queue_gpu import OpenCLQueue
from Simulation.data.geometry import Geometry
from Simulation.data.octree import Octree


class OpenCLBuffers:

    def __init__(self, context) -> None:
        self.buffers: dict[str, cl.Buffer] = dict()
        # Last kernel where this buffer as been involved or list of event where the buffer is involved
        self.event: cl.Event = None
        self.context: cl.Context = context

    def init_void_buffer(self, size) -> None:
        mf = cl.mem_flags
        self.point_size = size
        buffer = cl.Buffer(self.context, mf.READ_WRITE, size=size, hostbuf=None)
        self.buffers.update({"points": buffer})

    def init_from_oct(self, oct: Octree) -> None:
        mf = cl.mem_flags


        self.buffers.update({"octree": buffer_octree})

        if oct.primitives.size:
            self.prim_size = oct.primitives.size
            self.prim_shape = oct.primitives.shape
            buffer_primitives = cl.Buffer(
                self.context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=oct.primitives
            )
            self.buffers.update({"primitives": buffer_primitives})
        pass

    def init_from_geo(self, geo: Geometry) -> None:
        mf = cl.mem_flags

        self.point_shape = geo.points.shape
        self.point_size = geo.points.size
        buffer_point = cl.Buffer(self.context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=geo.points)
        self.buffers.update({"points": buffer_point})

        if geo.primitives.size:
            self.prim_size = geo.primitives.size
            self.prim_shape = geo.primitives.shape
            buffer_primitives = cl.Buffer(
                self.context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=geo.primitives
            )
            self.buffers.update({"primitives": buffer_primitives})

        if geo.variables:
            for name, val in geo.variables.items():
                if val.empty:
                    # buffer = cl.Buffer(self.context, mf.READ_WRITE, size=val.size)
                    buffer = cl.LocalMemory(val.size)
                elif val.uniform:
                    buffer = val.value
                else:
                    buffer = cl.Buffer(self.context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=val.value)
                self.buffers.update({f"var_{name}": buffer})
        if geo.groups:
            for name, val in geo.groups.items():
                buffer = cl.Buffer(self.context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=val.value)
                self.buffers.update({f"group_{name}": buffer})


    def update_cpu(self, geo: Geometry, queue: cl.CommandQueue) -> cl.Event:  # ??

        event = cl.enqueue_copy(queue, self.buffers["points"], geo.points)
        if geo.primitives:
            event = cl.enqueue_copy(queue, self.buffers["primitives"], geo.primitives)
        if geo.variables_point:
            for name, val in geo.variables_point.items():
                event = cl.enqueue_copy(queue, self.buffers[f"pt_var_{name}"], val)
        if geo.variables_prim:
            for name, val in geo.variables_prim.items():
                event = cl.enqueue_copy(queue, self.buffers[f"prim_var_{name}"], val)
        if geo.groups:
            for name, val in geo.groups.items():
                event = cl.enqueue_copy(queue, self.buffers[f"group_{name}"], val)

        return event

    def free(self) -> None:  ##Verif s'il y a des free à faire ??
        pass
