import unittest

from EngineeringToolbox import Frame, RotationMatrix, np


class TestRotationMatrix(unittest.TestCase):
    def test_simple_rotation(self):
        F = Frame()
        F.init_origin(0, 0, 0)
        F.init_axis((0, 1, 0),
                    (1, 0, 0),
                    (0, 0, 1))

        rot = RotationMatrix(0, np.pi, 0)

        from copy import deepcopy

        F_rot = deepcopy(F)
        F_rot.apply_rotation(rot)

        self.assertEqual(sum(F_rot.axis['x'].vector.round(5) == [0, 1, 0]), 3)
        self.assertEqual(sum(F_rot.axis['y'].vector.round(5) == [-1, 0, 0]), 3)
        self.assertEqual(sum(F_rot.axis['z'].vector.round(5) == [0, 0, -1]), 3)

        # Visualization
        #
        # Ox = F.origin.position['x']
        # Oy = F.origin.position['y']
        #
        # fig, (ax0, ax1) = plt.subplots(2, figsize=(5, 10))
        # ax0.plot([Ox, F.axis['x'].x], [Oy, F.axis['x'].y], label='x')
        # ax0.plot([Ox, F.axis['y'].x], [Oy, F.axis['y'].y], label='y')
        # ax0.legend()
        # ax1.plot([Ox, F_rot.axis['x'].x], [Oy, F_rot.axis['x'].y], label='x')
        # ax1.plot([Ox, F_rot.axis['y'].x], [Oy, F_rot.axis['y'].y], label='y')
        # ax1.legend()
        # plt.show()

    def test_complex_rotation(self):
        F = Frame()
        F.init_origin(4, 5.1, 0.2)

        F.init_axis((0, 1, 0),
                    (1, 0, 0),
                    (0, 0, 1))

        rot = RotationMatrix(1.2, np.pi, -0.4)

        from copy import deepcopy

        F_rot = deepcopy(F)
        F_rot.apply_rotation(rot)

        self.assertEqual(sum(F_rot.axis['x'].vector.round(5) == [0.14111, 0.33375, 0.93204]), 3)
        self.assertEqual(sum(F_rot.axis['y'].vector.round(5) == [-0.92106, 0.38942, 0.]), 3)
        self.assertEqual(sum(F_rot.axis['z'].vector.round(5) == [0.36295, 0.85846, -0.36236]), 3)