from __future__ import division

import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['text.antialiased'] = False
import cStringIO
import PIL
import random

from matplotlib import pyplot, colors, font_manager


def LOG(obj):
    print(obj)
    for name in dir(obj):
        if not name.startswith('__'):
            print('{} = {}'.format(name, getattr(obj, name)))
    print('')


class Canvas(object):
    SIZE = (200, 60)
    MARGIN = 10
    DPI = 80

    def __init__(self):
        self.color = colors.hsv_to_rgb([
            random.uniform(0, 1),
            random.uniform(0, 1),
            random.uniform(0, 1),
        ])
        self.num_digits = random.choice([5, 6])
        self.num_rectangles = random.randint(10, 40)

    def random_digits(self):
        self.digits = []
        for num_digit in xrange(self.num_digits):
            digit = Digit(
                x=random.uniform(
                    num_digit / self.num_digits + Canvas.MARGIN / Canvas.SIZE[0],
                    (num_digit + 1) / self.num_digits - Canvas.MARGIN / Canvas.SIZE[0],
                ),
                y=random.uniform(
                    0 + Canvas.MARGIN / Canvas.SIZE[1],
                    1 - Canvas.MARGIN / Canvas.SIZE[1],
                ),
            )
            self.digits.append(digit)

        self.s = ''.join([digit.s for digit in self.digits])

    def random_rectangles(self):
        self.rectangles = []
        for num_rectangles in xrange(self.num_rectangles):
            rectangle = Rectangle(
                x=random.uniform(0, 1),
                y=random.uniform(0, 1),
                w=random.uniform(0, 0.2),
                h=random.uniform(0, 0.6),
            )
            self.rectangles.append(rectangle)

    def render(self):
        self.fig = pyplot.figure(
            figsize=(Canvas.SIZE[0] / Canvas.DPI, Canvas.SIZE[1] / Canvas.DPI),
        )
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_axis_off()
        self.ax.set_xlim([0, 1])
        self.ax.set_ylim([0, 1])

        for item in self.digits + self.rectangles:
            item.render(self.ax)

    def save(self):
        buf = cStringIO.StringIO()

        self.fig.savefig(
            buf,
            dpi=Canvas.DPI,
            facecolor=self.color,
            format='png',
            bbox_inches=0,
            pad_inches=0,
        )

        image = PIL.Image.open(buf)
        image.save('{}.jpg'.format(self.s), quality=random.randint(30, 95))

    def close(self):
        pyplot.close(self.fig)


class Digit(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.s = str(random.randint(0, 9))
        self.zorder = random.random()
        self.rotation = random.uniform(-80, 80)
        self.color = colors.hsv_to_rgb([
            random.uniform(0, 1),
            random.uniform(0, 1),
            random.uniform(0, 1),
        ])
        self.font_properties = font_manager.FontProperties(
            family=random.choice(['Times New Roman', 'Courier New']),
            weight='bold',
            size=random.randint(16, 32),
        )

    def render(self, ax):
        ax.text(
            x=self.x,
            y=self.y,
            s=self.s,
            zorder=self.zorder,
            rotation=self.rotation,
            color=self.color,
            font_properties=self.font_properties,
            horizontalalignment='center',
            verticalalignment='center',
        )


class Rectangle(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.is_well = random.randint(0, 1)
        self.colorw = (1, 1, 1, random.uniform(0, 1))
        self.colork = (0, 0, 0, random.uniform(0, 1))
        self.zorder = random.random()

    def render(self, ax):
        x0 = self.x - self.w / 2
        x1 = self.x + self.w / 2
        y0 = self.y - self.h / 2
        y1 = self.y + self.h / 2

        ax.plot(
            [x0, x1, x1],
            [y0, y0, y1],
            color=self.colorw if self.is_well else self.colork,
            zorder=self.zorder,
        )
        ax.plot(
            [x0, x0, x1],
            [y0, y1, y1],
            color=self.colork if self.is_well else self.colorw,
            zorder=self.zorder,
        )


for _ in xrange(16):
    canvas = Canvas()
    canvas.random_digits()
    canvas.random_rectangles()
    canvas.render()
    canvas.save()
    canvas.close()
