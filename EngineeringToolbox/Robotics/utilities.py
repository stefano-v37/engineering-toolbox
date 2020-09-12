import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D, proj3d

THIS_DIR = os.path.dirname(os.path.realpath(__file__))


class Arrow3D(FancyArrowPatch):
    # from https://stackoverflow.com/a/22867877
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)

class Plotter:


    @classmethod
    def add_vector(cls, ax, vectors, color, **kwargs):
        for vector in vectors:
            if vector.__class__.__name__ == 'Axis':
                points = [[vector.origin.vector[i], vector.end.vector[i]] for i in range(len(vector.vector))]
                ax.plot(points[0],
                       points[1],
                       points[2],
                       color=color)
                if kwargs.get('arrow'):
                    a = Arrow3D(points[0],
                                points[1],
                                points[2],
                                mutation_scale=kwargs.get('mutation_scale', 10),
                                arrowstyle=kwargs.get('arrowstyle', "-|>"),
                                color=color)
                    ax.add_artist(a)

    @classmethod
    def show(cls, vectors, color, **kwargs):
        fig = plt.figure(figsize=(16,9))
        ax = fig.add_subplot(111, projection='3d')
        cls.add_vector(ax, vectors, color=color, **kwargs)