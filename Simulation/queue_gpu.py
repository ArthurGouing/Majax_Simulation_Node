import numpy as np
import pyopencl as cl


class OpenCLQueue:
    queue:cl.CommandQueue = None

    def __init__(self, context: cl.Context) -> None:
        queue = cl.CommandQueue(context)
        return

    def info(self): # si possible get des info genres, memory , nb ope, ect...
        pass
        
