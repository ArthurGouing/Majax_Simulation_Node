# Geometry type used for computation over blender obeject data
import numpy as np
from .variable import Variable

"""
x,y,z coordonate of the point
"""


class Point:

    def __init__(self, x: float, y: float, z: float) -> None:
        """Init x, y, z values"""
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def __getitem__(self, item: int) -> float:
        """
        Permit to access Point data as a list.
        example: Point[0] == Point.x
        """
        if item == 0:
            return self.x
        if item == 1:
            return self.y
        if item == 2:
            return self.z


"""
Prim for primitives, contain a list of point, which can be link to create a primitive.
it can be Line, Triangle, Quadrilateral, Tetrahedron. They can be uses for computation
or to represente the face  of the geometry for displaying the geometry.
"""
type_len = {"Line": 2, "Triangle": 3, "Quadrilateral": 4, "Tetrahedron": 4}


class Prim:

    def __init__(self, type_name: str, indices: list[int]) -> None:
        """Init the type and indices values"""
        self.type: str = type_name  # Choice between ["Line", "Triangle", "Tetrahedron", "Quadrilateral"]
        self.indices: list[int] = list()
        # if init with list
        if len(indices) != type_len[self.type]:
            print("ERROR")
            return
        self.indices = indices

    def __getitem__(self, item) -> int:
        """Permit to use prim[0] to acces indices values"""
        return self.indices[item]


"""
Geometry is a data class which contain the information of the geometry for the computation.
Using the geometry is faster and more handy compared to bpy.types.object
"""
Groupe = list[int]


class Geometry:

    def __init__(self, points: list[list[float]] = None, primitives: list[list[int]] = None) -> None:
        """Initialize the Geometry with eventual points and primitives values"""
        # List of all points and primitives of the geometry. The base data to represent a geometry
        # self.points:     list[Point] = list()
        self.points: np.ndarray[float, float] = np.array([])
        # self.primitives: list[Prim]  = list()
        self.primitives: np.ndarray[int, int] = np.array([])
        # List of variables attached to the geometry (can be non uniform variable)
        self.variables_point: dict[str, Variable] = dict()
        self.variables_prim: dict[str, Variable] = dict()
        # List of point indices to create a group of the geometry
        self.groups: dict[str, Groupe] = dict()
        if points:
            self.points = np.array(points, dtype=np.float32)  # TODO: option to choose precision
            if primitives:  # Primitive can existe only if points exist
                # self.prim_len = type_len[len(primitives[0])]
                self.primitives = np.array(primitives, dtype=np.int32)

    def add_point(self, point: Point) -> None:
        """Add a point to the list of point"""
        p = np.array([point.x, point.y, point.z])
        np.append(self.points, [p])

    def add_prim(self, prim: Prim) -> None:
        """Add a prim to the list of prim"""
        prim = np.array(prim.indices)
        np.append(self.primitives, [prim])

    def update_variable_point(self, name: str, var: Variable) -> None:
        """Create or update variable on points"""
        self.variables_point.update({name: var})

    def update_variable_prim(self, name: str, var: Variable) -> None:
        """Create or update variable on primitives"""
        self.variables_prim.update({name: var})

    def add_group(self, group: Groupe) -> None:
        """Add a groupe to the geometry"""
        self.groups.append(group)

    def delete_variable_point(self, name: str) -> None:
        """Delete the name variable"""
        self.variables_point.pop(name)

    def delete_variable_primitives(self, name: str) -> None:
        """Delete the name variable"""
        self.variables_prim.pop(name)

    def delete_group(self, name: str) -> None:
        """Delete the group named name"""
        self.groups.pop(name)

    def __add__(self, geo) -> None:  # Geometry
        """Merge operator: concatenate the data list"""
        self.points = np.concatenate(self.points, geo.points)  # axis=0
        self.primitives = np.concatenate(self.primitives, geo.primitives)  # axis=0
        return self

    def __getitem__(self, item) -> np.ndarray[float]:
        """Get the point i"""
        return self.points[item]

    def get_prim(self, item) -> np.ndarray[int]:
        return self.primitives[item]
