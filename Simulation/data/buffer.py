import numpy as np
import pyopencl as cl

from Simulation.queue_gpu import OpenCLQueue


## Quand on update les buffers, Ce sont des kernels en soit, il faudra les faire dans kernel ?

class OpenCLBuffer:
    context: cl.Context
    queue: cl.CommandQueue
    cpu_buffer: cl.Buffer
    gpu_buffer: cl.Buffer
    event: cl.Event # Last kernel where this buffer as been involved or list of event where the buffer is involved
    name: str

    def __init__(self, data: object) -> None:
        mf = cl.mem_flags
        self.name = data.name
        self.cpu_buffer = np.array(data) # to extenx
        self.gpu_buffer = cl.Buffer(self.context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = self.cpu_buffer)


    def update_cpu(self) -> cl.Event: # ??
        event = cl.enqueue_copy(self.queue, self.cpu_buffer, self.gpu_buffer)
        return event

    def update_gpu(self) -> cl.Event: # ??
        event = cl.enqueue_copy(self.queue, self.gpu_buffer, self.cpu_buffer)
        return event

    def free(self) -> None: ##Verif s'il y a des free à faire ??
        pass
