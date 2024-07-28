#################################################
# Copyright (C) 2025 Arthur Gouinguenet - All Rights Reserved
# This file is part of Majax Simulation Node project which is
# delivered under GNU General Public Liscense.
# For any questions or requests related to the use of this work
# please contact me directly at arthur.gouinguenet@free.fr
#############################################################


#### Library Import ####
import numpy as np
from copy import deepcopy

#### Blender Import ####
import bpy
from bpy.types import Object

#### Local Import #### 
from .variable import Variable


class AABB:
    def __init__(self, points: np.ndarray, option: str="") -> None:
        # Max point
        self.p_max: np.ndarray[float, float, float] = np.array([-float('inf'), -float('inf'), -float('inf')])
        # Min point
        self.p_min: np.ndarray[float, float, float] = np.array([ float('inf'),  float('inf'),  float('inf')])

        # Find Bound values
        if option=="Root":
            self.find_smallest_box(points)

    def find_smallest_box(self, points: np.ndarray) -> None:
        # compute the values of p_max and p_min
        self.p_max = np.array([-float('inf'), -float('inf'), -float('inf')])
        self.p_min = np.array([ float('inf'),  float('inf'),  float('inf')])
        for p in points:
            # Set p_max
            if p[0] > self.p_max[0]:
                self.p_max[0]=p[0]
            if p[1] > self.p_max[1]:
                self.p_max[1]=p[1]
            if p[2] > self.p_max[2]:
                self.p_max[2]=p[2]

            # Set p_min
            if p[0] < self.p_min[0]:
                self.p_min[0]=p[0]
            if p[1] < self.p_min[1]:
                self.p_min[1]=p[1]
            if p[2] < self.p_min[2]:
                self.p_min[2]=p[2]


class OctNode:
    def __init__(self, aabb, points) -> None:
        """Warn some node can be void : no points neither childs"""
        # AABB Box
        self.box = aabb
        # Childs
        self.childs: list[OctNode] = []

        # Init
        self.leaf_size = 128
        self.id_print = 1

        if len(points)>self.leaf_size:
            self.points: np.ndarray[float] = points
            # Find the a repartition of point i;e fill repartitions
            repartitions = self.find_repartitions()
            # Split point so they respect the repartition
            points_list = list()
            self.split(points, repartitions, 2, points_list, self.box)
    
    def print(self, msg):
        print(msg, sep=": ")
        if self.is_leaf:
            print(f"{self.leaf_size} leaves")
        else:
            for i, oct in enumerate(self.childs):
                print(f"branch {i} | ", sep="")
        

    def find_repartitions(self) -> list[int]:
        """Compute how much point per AABB"""
        # Is it better to order the repartition list ? specially case where there is 0 
        n = len(self.points)
        k = self.circle(n)
        p1 = n//(self.leaf_size*8**k)
        n1 = n%(self.leaf_size*8**k)
        repartitions = p1 * [self.leaf_size*8**k]
        if p1==8:
            return repartitions
        # il reste a remplir 8-r esspaces
        pi = 1 ; ni = n1
        while p1<7 or ni < self.leaf_size:
            k = self.circle(n1)
            pi = ni//(self.leaf_size*8**k)
            if pi > 8-p1-1: # Assure qu'il y est moi de 8 repartitions
                pi = 8-p1-1
            elif pi==0:
                repartitions += (7-p1) * [0]
                break
            ni = ni -pi*self.leaf_size*8**k 
            repartitions += pi * [self.leaf_size*8**k]
            p1=p1+pi # Le nombre de sous-cube deja rempli
        repartitions += [ni]
        print("repartition: ", repartitions, "(len = ", len(repartitions), ")")
        return repartitions
    
    def circle(self, n: int) -> int:
        # Find the k s.t. 16**k < n < 16**k+1
        k = 0
        while self.leaf_size*8**(k+1)<n:
            k+=1
        return k

    def is_leaf(self):
        return all(child is None for child in self.children)

    def split(self, points: np.ndarray, quantity: list[int], axis: int, points_list: list[np.ndarray], box: AABB) -> tuple[list[np.ndarray, AABB]]:
        """ Recursive function which split the point in two according to the quantity list allong one axis by level"""
        if axis==-1:
            points_list.append({"box":box, "points": points})
            self.id_print += 1
            box.find_smallest_box(points)
            print(self.id_print, "box", box.__dict__, " |   points: ", len(points))
            bpy.ops.mesh.primitive_cube_add(size=1, location=(box.p_max+box.p_min)/2, scale=box.p_max-box.p_min)
            self.childs.append(OctNode(box, points))
            return
        # Handle case where there is no points to splits
        if len(points)==0:
            axis = axis + 1
            return points_list

        new_points_list = list()
        # q is the number of the half
        q = sum(quantity[:len(quantity)//2], 0)
        p, pts1, pts2 = self.compute_median(points, q, axis)
        # Build boxes
        box_1 = deepcopy(box) # .p_max
        box_1.p_max[axis] = p
        box_2 = deepcopy(box) # .p_min[axis]
        box_2.p_min[axis] = p
        
        # p est le point par lequel pace le plan orthogonale à l'axe axis, qui coupe points en 2 selon q
        # pts1 est la  liste des points qui sont plus petit que p
        # pts2 est la liste des points qui sont plus grqnd que p (selon l'axe)
        # On a besoin de p pour créer  les boites
        axis = axis - 1
        self.split(pts1, quantity[:2**(axis+1)], axis, points_list, box_1)
        self.split(pts2, quantity[2**(axis+1):], axis, points_list, box_2)
        axis = axis + 1
        return new_points_list

    def compute_median(self, points: np.ndarray, quantity: int, axis: int) -> list[float, np.ndarray, np.ndarray]:
        """Return the left list, the right list and the median point"""
        # Initialization
        n = len(points)
        arr = [p[axis] for p in points]

        # TODO should be handled by the quick select

        # n is paire
        if n%2==0:
            v_left  = self.quick_select(arr, 0, n-1, quantity)
            if quantity<n:
                v_right = self.quick_select(arr, 0, n-1, quantity+1)
            else:
                v_right = v_left
            v_med = (v_left + v_right) / 2

        # n is odd
        else:
            v_med = self.quick_select(arr, 0, n-1, quantity)

        p_left = [p for p in points if p[axis]<v_med] # ERROR some point == p_med -> len(p_left /= quantity)
        p_right = [p for p in points if p[axis]>v_med]
        p_med = [p for p in points if p[axis]==v_med]
        # Split p_med to p_left and p_right s.t. len(p_left)==quantity
        k = quantity-len(p_left)
        p_left = p_left + p_med[:k]
        p_right = p_right + p_med[k:]

        # Test for error
        if len(p_left) +len(p_right) != n:
            print("Error: forgot to count points when splitting points")

        return v_med, p_left, p_right

    def quick_select(self, arr: list[float], left: int, right: int, quantity: int)-> float:
       # Partition the array around last 
       # element and get position of pivot 
       # element in sorted array 
       index = self.partition(arr, left, right) 
       # Correction should be in the upper function...
       # if we want 0 point, we create a box from the value of the 1st points.
       # so we must put quantity to 1 to allow quick select to work correctly 
       quantity = 1 if quantity==0 else quantity
  
       # if position is same as k 
       if (index - left == quantity - 1): 
           return arr[index] 
  
       # If position is more, recur  
       # for left subarray  
       if (index - left > quantity - 1): 
           return self.quick_select(arr, left, index - 1, quantity) 
  
       # Else recur for right subarray  
       return self.quick_select(arr, index + 1, right, quantity - index + left - 1) 

    def partition(self, arr: list[float], l: int, r: int) -> int:
        x = arr[r] 
        i = l 
        for j in range(l, r): 
              
            if arr[j] <= x: 
                arr[i], arr[j] = arr[j], arr[i] 
                i += 1
                  
        arr[i], arr[r] = arr[r], arr[i] 
        return i 


class Octree:
    def __init__(self, points: list[list[float]] = None, primitives: list[list[int]] = None, dtype: np.dtype = np.single) -> None:
        # Root
        self.root: OctNode = None
        # Maximum depth of the tree
        self.max_depth: int = None
        # Number of point of the octree mesh
        self.size = len(points)
        # Liste des primitives ( faces, edges ou thetradèdre )
        self.primitives: np.ndarray[int, int] = np.array([])
        # List of variables attached to the geometry (can be non uniform variable)
        self.variables: dict[str, Variable] = dict()
        # List of point indices to create a group of the geometry
        self.groups: dict[str, Groupe] = dict()
        # (Utile pour savoir si 2 points sont voisin et si il faut tester la collisiton entre eux 2)
        # il faut plutot une liste de voisin, ou la liste d'element et pout chaque point,
        # une liste des elements auquelle ils appartiennent.
        self.build(np.array(points, dtype=dtype), primitives)
        self.print()

    def print(self, depth=1):
        d = 1
        nodes = [self.root] 
        while d < depth or nodes==[]:
            print("\n---- Depth {d} ----", end="")
            [n.print(f"Node {i}") for i, n in enumerate(nodes)]
            nodes = sum([n.childs for n in nodes], [])
            d+=1
    def insert(self, node, bound, points):
        pass

    def subdivide(self, node):
        pass

    def get_octan_index(self, bound, points):
        # Toube l'index du child en fonction des points et des bounds
        pass

    def get_child_bound(self, bounds, index):
        pass

    def build(self, points: np.ndarray, primitives: np.ndarray):
        self.prim = primitives
        box = AABB(points, option="Root")
        self.root = OctNode(box, points)
        pass

