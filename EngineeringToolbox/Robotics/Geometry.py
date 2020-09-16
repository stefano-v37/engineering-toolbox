"""
.py with geometry objects
There are no reference to origins, therefore the frame is fixed to __F__
"""

import numpy as np


class Point:

    def __init__(self, xyz):
        x, y, z = xyz
        self.x = x
        self.y = y
        self.z = z
        self.val = dict(x=x, y=y, z=z)
        self.calculate_vector()

    def calculate_vector(self):
        self.vector = np.array([self.x, self.y, self.z])

    def update(self):
        self.x = self.val['x']
        self.y = self.val['y']
        self.z = self.val['z']
        self.calculate_vector()

class Line:
    def __init__(self, O, xyz):
        self.origin = Point(O)
        self.end = Point(xyz)
        self.vector = self.calculate_vector()
        self.update()

    def calculate_length(self):
        self.length = np.sqrt(sum([(self.end.val[coord] - self.origin.val[coord])**2 for coord in ['x', 'y', 'z']]))

    def calculate_vector(self):
        return self.end.vector - self.origin.vector

    def update(self):
        self.end.update()
        self.calculate_length()
        self.vector = self.calculate_vector()


class Vector(Line):

    def __init__(self, xyz):
        Line.__init__(self, O=[0,0,0], xyz = xyz)
        self.homogeneous = np.append(self.vector, [1])
        self.calculate_cosine_directors()

    def calculate_cosine_directors(self):
        self.cosine_directors ={axis : self.end.val[axis]/self.length for axis in ['x', 'y', 'z']}

    def scale(self, factor):
        axis_name = ['x', 'y', 'z']
        if isinstance(factor, dict):
            factor_dict = factor
        if isinstance(factor, list):
            factor_dict = {axis_name[i]: factor[i] for i in range(len(axis_name))}
        else:
            new_length = self.length * factor
            factor_dict = {axis: self.cosine_directors[axis]*new_length for axis in axis_name}

        for axis in axis_name:
            self.end.val[axis] *= factor_dict[axis]
        self.update()






    # def apply_rotation(self, rot, inplace=False, new=True):
    #     # preliminary version: based on fixed origin and fixed frame
    #     # successive rotation are peformed on the actual rotated fixed frame
    #     # TODO: why??
    #     # .apply_rotation(1) -> .apply_rotation(2) == .apply_rotation([2,1])
    #     ### FIXED FRAME POV:
    #     ### rot = [rot3, rot2, rot1]; .apply_rotation(1), .apply_rotation(2), .apply_rotation(3)
    #     ###
    #     ##### PREVIOUS FRAME POV:
    #     ##### rot = [rot1, rot2, rot3]; .apply_rotation(3), .apply_rotation(2), .apply_rotation(1)
    #     ##### NOTE THAT IT STARTS WITH FIXED FRAME, THEREFORE IF YOU ROTATE AN ALREADY ROTATED FRAME IT WON'T BE COORDINATED
    #     if type(rot) is np.ndarray:
    #         rot = [rot]
    #     rot_end = rot + [self.end.vector]
    #     rotated = np.linalg.multi_dot(rot_end)
    #     rot_origin = rot + [self.origin.vector]
    #     o_rotated = np.linalg.multi_dot(rot_origin)
    #
    #     if inplace:
    #         self.__dict__.update(Line(rotated, origin=Point(o_rotated)).__dict__)
    #         if new:
    #             return self
    #     else:
    #         return rotated

class Versor(Vector):
    pass