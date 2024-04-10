# Geometry type used for computation over blender obeject data
import numpy as np
from .variable import Variable

"""
x,y,z coordonate of the point
"""
class Point:
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float) -> None:
        """ Init x, y, z values"""
        self.x = x
        self.y = y
        self.z = z

    def __getitem__(self, item: int) -> float:
        """
        Permit to access Point data as a list. 
        example: Point[0] == Point.x
        """
        if item==0:
            return self.x
        if item==1:
            return self.y
        if item==2:
            return self.z


"""
Prim for primitives, contain a list of point, which can be link to create a primitive.
it can be Line, Triangle, Quadrilateral, Tetrahedron. They can be uses for computation
or to represente the face  of the geometry for displaying the geometry.
"""
type_len = {"Line": 2, "Triangle": 3, "Quadrilateral": 4, "Tetrahedron": 4}
class Prim:
    type: str          = "Line"  # Choice between ["Line", "Triangle", "Tetrahedron", "Quadrilateral"]
    indices: list[int] = list()

    def __init__(self, type: str, indices: list[int]) -> None:
        """ Init the type and indices values"""
        self.type = type
        # if init with list
        if len(indices)!=type_len[type]: print("ERROR"); return
        self.indices = indices

    def __getitem__(self, item) -> int:
        """ Permit to use prim[0] to acces indices values"""
        return self.indices[item]


"""
Geometry is a data class which contain the information of the geometry for the computation.
Using the geometry is faster and more handy compared to bpy.types.object
"""
Groupe = list[int]
class Geometry:
    # List of all points and primitives of the geometry. The base data to represent a geometry
    points:     list[Point] = list()
    primitives: list[Prim]  = list() 
    # List of variables attached to the geometry (can be non uniform variable)
    variables_point: dict[str, Variable] = dict()
    variables_prim:  dict[str, Variable] = dict()
    # List of point indices to create a group of the geometry
    groupes: list[Groupe] = list()

    def __init__(self, points: list[Point]=None, primitives: list[Prim]=None) -> None:
        """Initialize the Geometry with eventual points and primitives values"""
        if points:
            self.points = points
        if primitives:
            self.primitives = primitives

    def add_point(self, point: Point) -> None:
        """Add a point to the list of point"""
        self.points.append(point)
    def add_prim(self, prim: Prim) -> None:
        """Add a prim to the list of prim"""
        self.primitives.append(prim)

    def update_variable_point(self, name: str, var: Variable) -> None:
        """Create or update variable on points"""
        self.variables_point.update({name, var})
    def update_variable_prim(self, name: str, var: Variable) -> None:
        """Create or update variable on primitives"""
        self.variables_prim.update({name: var})

    def delete_variable_point(self, name: str) -> None:
        """Delete the name variable"""
        self.variables_point.pop(name)
    def delete_variable_primitives(self, name: str) -> None:
        """Delete the name variable"""
        self.variables_prim.pop(name)

    def add_groupe(self, group: Groupe) -> None:
        """Add a groupe to the geometry"""
        self.groupes.append(group)

    def __add__(self, geo) -> None: # Geometry
        """Merge operator: concatenate the data list"""
        new_geo = Geometry()
        new_geo.points = self.points + geo.points
        new_geo.primitives = self.primitives + geo.primitives
        return new_geo