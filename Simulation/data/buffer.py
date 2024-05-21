import numpy as np
import pyopencl as cl

from Simulation.queue_gpu import OpenCLQueue
from Simulation.data.geometry import Geometry


## Quand on update les buffers, Ce sont des kernels en soit, il faudra les faire dans kernel ?


class OpenCLBuffers:

    def __init__(self, context) -> None:
        self.buffers: dict[str, cl.Buffer] = dict()
        # Last kernel where this buffer as been involved or list of event where the buffer is involved
        self.event: cl.Event = None
        self.context: cl.Context = context

    def init_void_buffer(self, size) -> None:
        mf = cl.mem_flags
        self.point_size = size
        buffer = cl.Buffer(self.context, mf.READ_ONLY | mf.COPY_HOST_PTR, size=size)
        self.buffers.update({"points": buffer})

    def init_from_geo(self, geo: Geometry) -> None:
        mf = cl.mem_flags

        # Get geo adress i.e. data_id_name ???

        self.point_size = geo.points.shape
        buffer_point = cl.Buffer(self.context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=geo.points)
        self.buffers.update({"points": buffer_point})

        if geo.primitives.size:
            self.prim_size = geo.primitives.shape
            buffer_primitives = cl.Buffer(
                self.context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=geo.primitives
            )
            self.buffers.update({"primitives": buffer_primitives})

        if geo.variables_point:
            for name, val in geo.variables_point.items():
                buffer = (
                    cl.Buffer(self.context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=val.value)
                    if not val.uniform
                    else val.value  # should already be a numpy, but it is a precotion
                )
                self.buffers.update({f"pt_var_{name}": buffer})
        if geo.variables_prim:
            for name, val in geo.variables_prim.items():
                buffer = (
                    cl.Buffer(self.context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=val.value)
                    if not val.uniform
                    else val.value
                )
                self.buffers.update({f"prim_var_{name}": buffer})
        if geo.groups:
            for name, val in geo.groups.items():
                buffer = cl.Buffer(self.context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=val.value)
                self.buffers.update({f"group_{name}": buffer})

    def update_gpu(self, geo: Geometry) -> cl.Event:  # ??
        # TODO: usefull for converter node. I don't see a case where it is usefull as
        # all buffer must be used in the simulation loop ...
        pass

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
