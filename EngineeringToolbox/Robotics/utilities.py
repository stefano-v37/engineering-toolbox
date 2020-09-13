import matplotlib.pyplot as plt
import numpy as np
import os
import yaml
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D, proj3d
import traceback
import inspect, itertools

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

conf_path = THIS_DIR + '\\configuration.yml'
with open(conf_path) as configuration:
    configuration = yaml.safe_load(configuration)


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
    def variablename(cls, var):
        return [tpl for tpl in filter(lambda x: var is x[1], globals().items())]

    @classmethod
    def getvariablename(cls, var):
        stack = traceback.extract_stack()
        _, _, _, get = stack[-2]
        return get[16:-1]

    @classmethod
    def getvariablename2(cls, variable):
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = string[string.find('(') + 1:-1].split(',')

        names = []
        for i in args:
            if i.find('=') != -1:
                names.append(i.split('=')[1].strip())

            else:
                names.append(i)

        return names[0]

    @classmethod
    def add_vector(cls, ax, vectors, **kwargs):
        colors = kwargs.get('colors', None)
        if type(colors) is str:
            colors = [colors for x in range(len(vectors))]
        elif colors == None:
            colors = [None for x in range(len(vectors))]

        i = 0
        j = 0
        labels = kwargs.get('labels', [None for x in range(len(vectors))])
        for vector in vectors:
            if vector.__class__.__name__ == 'Frame':
                j += 3
                k = 0
                for axis in vector.axes:
                    if labels[i] is None:
                        labels[i] = [None for x in range(len(vector.axes))]
                    if type(colors[i]) is str:
                        colors[i] = [colors[i] for x in range(len(vector.axes))]
                    elif colors[i] == None:
                        colors[i] = [None for x in range(len(vectors.axes))]
                    # vectorname = cls.variablename(axis).replace('__', '')
                    points = [[axis.origin.vector[i], axis.end.vector[i]] for i in range(len(axis.vector))]
                    ax.plot(points[0],
                            points[1],
                            points[2],
                            color=colors[i][k],
                            label=labels[i][k])
                    a = Arrow3D(points[0],
                                points[1],
                                points[2],
                            mutation_scale=kwargs.get('mutation_scale', 10),
                            arrowstyle=kwargs.get('arrowstyle', "-|>"), color=colors[i][k])
                    ax.add_artist(a)
                    k += 1
                i += 1
            if vector.__class__.__name__ == 'Axis':
                j += 1
                points = [[vector.origin.vector[i], vector.end.vector[i]] for i in range(len(vector.vector))]
                ax.plot(points[0],
                        points[1],
                        points[2],
                        color=colors[i],
                        label=labels[i])
                a = Arrow3D(points[0],
                            points[1],
                            points[2],
                            mutation_scale=kwargs.get('mutation_scale', 10),
                            arrowstyle=kwargs.get('arrowstyle', "-|>"),
                            color=colors[i])
                ax.add_artist(a)
                i += 1
            if vector.__class__.__name__ == 'Point':
                j += 1
                points = vector.vector
                print(points)
                ax.scatter(points[0],
                           points[1],
                           points[2],
                           color=colors[i],
                           label=labels[i])
                i += 1
            legend = kwargs.get('legend', False)
            if legend:
                ax.legend(ncol=j)
        # workaround to set aspect_ratio equal
        # source: https://github.com/matplotlib/matplotlib/issues/17172#issuecomment-615850047
        lims = np.array([ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d()]).T
        lim = [min(lims[0]), max(lims[1])]
        ax.set_xlim3d(lim)
        ax.set_ylim3d(lim)
        ax.set_zlim3d(lim)

    @classmethod
    def show(cls, vectors, **kwargs):
        figsize = kwargs.get('figsize', (configuration['Plotter']['figsize'][0],configuration['Plotter']['figsize'][1]))
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')
        cls.add_vector(ax, vectors, **kwargs)