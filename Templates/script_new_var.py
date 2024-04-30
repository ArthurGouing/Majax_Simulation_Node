# Alias
# @ALIAS@ Geometry_inout@a

# Import Libraries
import bpy
from Simulation import Geometry, Variable # Pas sur que les users est accés à ca et que mon histoire compilera bien
# import Majax custom data types !?

def script(a: Geometry):
    # Set uniform variable on point
    m = 0.1 # Kg
    var = Variable(m, uniform=True)
    a.update_variable_point("mass", var)

    # Compute L0 for each edge
    l0 = list()
    for e in a.primitives:
        l0.append(abs(e[0]-e[1]))
    var_l0 = Variable(l0, uniform=False)
    a.update_variable_prim("l0", var_l0)
    
