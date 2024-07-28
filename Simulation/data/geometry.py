# Geometry type used for computation over blender obeject data
import numpy as np
from .variable import Variable

type_len = {"Line": 2, "Triangle": 3, "Quadrilateral": 4, "Tetrahedron": 4}

"""
Geometry is a data class which contain the information of the geometry for the computation.
Using the geometry is faster and more handy compared to bpy.types.object
"""
Groupe = list[int]


class Geometry:

    def __init__(self, points: list[list[float]] = None, primitives: list[list[int]] = None, dtype: np.dtype = np.single) -> None:
        """Initialize the Geometry with eventual points and primitives values"""
        # List of all points and primitives of the geometry. The base data to represent a geometry
        # self.points:     list[Point] = list()
        self.points: np.ndarray[float, float] = np.array([])
        # self.primitives: list[Prim]  = list()
        self.primitives: np.ndarray[int, int] = np.array([])
        # List of variables attached to the geometry (can be non uniform variable)
        self.variables: dict[str, Variable] = dict()
        # List of point indices to create a group of the geometry
        self.groups: dict[str, Groupe] = dict()
        # dtype
        self.dtype = dtype
        if points:
            self.points = np.array(points, dtype=dtype)
            if primitives:  # Primitive can existe only if points exist
                # self.prim_len = type_len[len(primitives[0])]
                self.primitives = np.array(primitives, dtype=np.int32)

    def add_point(self, point: np.ndarray[float]) -> None:
        """Add a point to the list of point"""
        p = np.array([point.x, point.y, point.z])
        np.append(self.points, [p])

    def add_prim(self, prim: np.ndarray[int]) -> None:
        """Add a prim to the list of prim"""
        prim = np.array(prim.indices)
        np.append(self.primitives, [prim])

    def update_variable(self, name: str, var: Variable) -> None:
        """Create or update variable on points"""
        self.variables.update({name: var})

    def add_group(self, group: Groupe) -> None:
        """Add a groupe to the geometry"""
        self.groups.append(group)

    def delete_variable(self, name: str) -> None:
        """Delete the name variable"""
        self.variables.pop(name)

    def delete_group(self, name: str) -> None:
        """Delete the group named name"""
        self.groups.pop(name)

    def __add__(self, geo) -> None:  # Geometry
        """Merge operator: concatenate the data list"""
        self.points = np.concatenate(self.points, geo.points)  # axis=0
        self.primitives = np.concatenate(self.primitives, geo.primitives)  # axis=0
        return self

    def __getitem__(self, item) -> np.ndarray[np.single|np.double]:
        """Get the point i"""
        return self.points[item]

    def get_prim(self, item) -> np.ndarray[int]:
        return self.primitives[item]
