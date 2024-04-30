# Alias
# ALIAS a = geometry_out
#@ALIAS@ geometry_2_in @ b
#@alias@ my_personal_name_in@c

# Import Libraries
import bpy
from Simulation import Geometry # Pas sur que les users est accés à ca et que mon histoire compilera bien

def script(a: Geometry, b: Geometry, c: Geometry):
    for i in range(len(a.points)):
        a.points[i] = b.points[i] * c.points[i]