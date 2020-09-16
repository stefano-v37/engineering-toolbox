import numpy as np
from .utilities import configuration

__X__ = np.array(configuration['StandardFrame']['X'])
__Y__ = np.array(configuration['StandardFrame']['Y'])
__Z__ = np.array(configuration['StandardFrame']['Z'])
__O__ = np.array(configuration['StandardFrame']['O'])

# class Point:
#
#     def __init__(self, xyz):
#         x, y, z = xyz
#         self.x = x
#         self.y = y
#         self.z = z
#         self.val = dict(x=x, y=y, z=z)
#         self.vector = self.vector()
#
#     def vector(self):
#         return np.array([self.x, self.y, self.z])


__O__ = Point(__O__)


# class Line:
#     def __init__(self, xyz, origin=None):
#         if origin:
#             self.origin = origin
#         else:
#             self.origin = __O__
#         self.end = Point(xyz)
#         self.vector = self.vector()
#         self.homogeneous = np.append(self.vector, [1])
#         self.length = self.calculate_length()
#         # self = self.__dict__
#
#     def vector(self):
#         return self.end.vector - self.origin.vector
#
#     def calculate_length(self):
#         return np.sqrt(sum([(self.end.val[coord] - self.origin.val[coord])**2 for coord in ['x', 'y', 'z']]))
#
#     def apply_rotation(self, rot, inplace=False, new=True):
#         # preliminary version: based on fixed origin and fixed frame
#         # successive rotation are peformed on the actual rotated fixed frame
#         # TODO: why??
#         # .apply_rotation(1) -> .apply_rotation(2) == .apply_rotation([2,1])
#         ### FIXED FRAME POV:
#         ### rot = [rot3, rot2, rot1]; .apply_rotation(1), .apply_rotation(2), .apply_rotation(3)
#         ###
#         ##### PREVIOUS FRAME POV:
#         ##### rot = [rot1, rot2, rot3]; .apply_rotation(3), .apply_rotation(2), .apply_rotation(1)
#         ##### NOTE THAT IT STARTS WITH FIXED FRAME, THEREFORE IF YOU ROTATE AN ALREADY ROTATED FRAME IT WON'T BE COORDINATED
#         if type(rot) is np.ndarray:
#             rot = [rot]
#         rot_end = rot + [self.end.vector]
#         rotated = np.linalg.multi_dot(rot_end)
#         rot_origin = rot + [self.origin.vector]
#         o_rotated = np.linalg.multi_dot(rot_origin)
#
#         if inplace:
#             self.__dict__.update(Line(rotated, origin=Point(o_rotated)).__dict__)
#             if new:
#                 return self
#         else:
#             return rotated


__X__ = Line(__X__)
__Y__ = Line(__Y__)
__Z__ = Line(__Z__)


class Frame:
    def __init__(self, items):
        self.size = len(items)
        self.axes_dict = {str(i) : items[i] for i in range(len(items))}
        self.axes = items
#         vectors in line
        self.vector = np.array([item.vector for _, item in self.axes_dict.items()])

    def apply_rotation(self, rot):
        temp = Frame([vector.apply_rotation(rot, inplace=True) for vector in self.axes])
        self.__dict__.update(temp.__dict__)



__F__ = Frame([__X__, __Y__, __Z__])

class OrientedLine(Line):
    def __init__(self, **kwargs):
        Line.__init__(self, **kwargs)
        self.__F__ = kwargs.get('frame', __F__)


class RotationMatrix:
    def __init__(self, gamma, beta, alpha):
        # around which axis
        self.rot_X = self.X_rot(alpha)
        self.rot_Y = self.Y_rot(beta)
        self.rot_Z = self.Z_rot(gamma)

    @classmethod
    def X_rot(cls, gamma):
        x_rotation = [1, 0, 0]
        y_rotation = [0, np.cos(gamma), -np.sin(gamma)]
        z_rotation = [0, np.sin(gamma), np.cos(gamma)]
        return np.array((x_rotation, y_rotation, z_rotation))

    @classmethod
    def Y_rot(cls, beta):
        x_rotation = [np.cos(beta), 0, np.sin(beta)]
        y_rotation = [0, 1, 0]
        z_rotation = [-np.sin(beta), 0, np.cos(beta)]
        return np.array((x_rotation, y_rotation, z_rotation))

    @classmethod
    def Z_rot(cls, alpha):
        x_rotation = [np.cos(alpha), -np.sin(alpha), 0]
        y_rotation = [np.sin(alpha), np.cos(alpha), 0]
        z_rotation = [0, 0, 1]
        return np.array((x_rotation, y_rotation, z_rotation))

    @classmethod
    def axis_angle(cls, axis, angle):
        x,y,z = axis.vector
        t = angle
        R1 = [np.cos(t) + (1-np.cos(t))*x**2, x*y*(1-np.cos(t)) - z*np.sin(t), x*z*(1-np.cos(t)) + y*np.sin(t)]
        R2 = [y*x*(1-np.cos(t)) + z*np.sin(t), np.cos(t) + (1-np.cos(t))*y**2, y*z*(1-np.cos(t)) - x*np.sin(t)]
        R3 = [z*x*(1-np.cos(t)) - y*np.sin(t), z*y*(1-np.cos(t)) + x*np.sin(t), np.cos(t) + (1-np.cos(t))*z**2]
        return np.array([R1, R2, R3])