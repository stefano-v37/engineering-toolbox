from .kinematics import __O__


class Robot:
    # target: connect the pose of the end-effector with parameters of the joints
    def __init__(self, joints):
        # joints is a ordered list of the joints of the robot
        pass

    def update(self, q):
        # q are the parameters of each joint
        pass

class Joint:
    def __init__(self, n_dof, dof, lengthorigin = __O__):
        """
        Joints are the solid links that form the robot
        :param n_dof: int : degree of freedom number
        :param dof: dict/list : dict with names of dof and initial value
        """

        self.n_dof = n_dof
        if isinstance(dof, dict):
            self.dof = dof
        elif isinstance(dof, list):
            self.dof = {dof_i : 0 for dof_i in dof}
    pass

class RotationalJoint(Joint):
    super(Joint, 1)


class CollinearJoint(Joint):
    super(Joint, 1)


class Ground(Joint):
    super(Joint, 0)