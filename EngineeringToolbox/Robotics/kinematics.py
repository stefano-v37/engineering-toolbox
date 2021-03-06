import numpy as np
import yaml

from EngineeringToolbox.Robotics.utilities import THIS_DIR

conf_path = THIS_DIR + '\\configuration.yml'
with open(conf_path) as configuration:
    configuration = yaml.safe_load(configuration)
    X = np.array(configuration['StandardFrame']['X'])
    Y = np.array(configuration['StandardFrame']['Y'])
    Z = np.array(configuration['StandardFrame']['Z'])

class Point:
    def set_position(self, x,y,z):
        self.position = dict(x=x, y=y, z=z)


class Axis:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vector = self.init_vector()

    def init_vector(self):
        return self.x * X + self.y * Y + self.z * Z

    def apply_rotation(self, rot):
        # rot is an instance of RotationMatrix
        if type(rot) is RotationMatrix:
            self.vector = self.vector.dot(rot.rot_X).dot(rot.rot_Y).dot(rot.rot_Z)
            self.x = self.vector[0]
            self.y = self.vector[1]
            self.z = self.vector[2]
        elif type(rot) is np.ndarray:
            self.vector = self.vector.dot(rot)
            self.x = self.vector[0]
            self.y = self.vector[1]
            self.z = self.vector[2]


class Frame:
    def init_origin(self, x_, y_, z_):
        self.origin = Point()
        self.origin.set_position(x_, y_, z_)

    def init_axis(self, X_, Y_, Z_):
        self.axis = dict(x=Axis(X_[0], X_[1], X_[2]), y=Axis(Y_[0], Y_[1], Y_[2]), z=Axis(Z_[0], Z_[1], Z_[2]))

    def apply_rotation(self, rot):
        # TODO: apply rotation directly to the matrix of the Frame
        for axis in ['x', 'y', 'z']:
            self.axis[axis].apply_rotation(rot)


class RotationMatrix:
    # TODO: develop also a method for rotating according to a different frame. This method is based for the standard origin
    def __init__(self, gamma, beta, alpha):
        self.rot_X = self.make_X_rot(gamma)
        self.rot_Y = self.make_Y_rot(beta)
        self.rot_Z = self.make_Z_rot(alpha)

    def make_X_rot(self, gamma):
        x_rotation = [1, 0, 0]
        y_rotation = [0, np.cos(gamma), np.sin(gamma)]
        z_rotation = [0, -np.sin(gamma), np.cos(gamma)]
        return np.array((x_rotation, y_rotation, z_rotation)).T

    def make_Y_rot(self, beta):
        x_rotation = [np.cos(beta), 0, -np.sin(beta)]
        y_rotation = [0, 1, 0]
        z_rotation = [np.sin(beta), 0, np.cos(beta)]
        return np.array((x_rotation, y_rotation, z_rotation)).T

    def make_Z_rot(self, alpha):
        x_rotation = [np.cos(alpha), -np.sin(alpha), 0]
        y_rotation = [np.sin(alpha), np.cos(alpha), 0]
        z_rotation = [0, 0, 1]
        return np.array((x_rotation, y_rotation, z_rotation)).T