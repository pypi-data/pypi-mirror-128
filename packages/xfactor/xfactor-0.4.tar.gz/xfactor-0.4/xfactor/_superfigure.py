#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sympy import symbols, nonlinsolve
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from ._superaxes3d import SuperAxes3D


class SuperFigure(Figure):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0:
            # Upgrade from an existing figure
            self.__dict__.update(**args[0].__dict__)
        else:
            # create new figure
            super().__init__(*args, **kwargs)
            # steal a canvas manager
            dummy = plt.figure()
            manager = dummy.canvas.manager
            manager.canvas.figure = self
            self.set_canvas(manager.canvas)

    @property
    def width_to_height(self):
        return self.get_figwidth() / self.get_figheight()

    def make_axes(self, left=None, right=None, top=None, bottom=None,
                  width=None, height=None, width_to_height=None,
                  style=None, **kwargs):
        '''

        Parameters
        ----------
        style: None or 'modern' or 'blank'
            Artistic style of the axes
        '''
        # solve for axes position
        # left, right, top, bottom, width, height, aspect_ratio
        l, r, t, b, w, h, a = symbols('l r t b w h a', real=True)
        eqns = [w + l - r, h + t - b, w - h * a]
        if left is not None:
            eqns.append(l - left)
        if right is not None:
            eqns.append(r - right)
        if top is not None:
            eqns.append(t - top)
        if bottom is not None:
            eqns.append(b - bottom)
        if width is not None:
            eqns.append(w - width)
        if height is not None:
            eqns.append(h - height)
        if width_to_height is not None:
            eqns.append(w / h - width_to_height / self.width_to_height)
        unknowns = [l, r, t, b, w, h, a]
        try:
            sols, = nonlinsolve(eqns, unknowns)
            left = float(sols[0])
            right = float(sols[1])
            top = float(sols[2])
            bottom = float(sols[3])
            width = float(sols[4])
            height = float(sols[5])
            width_to_height = float(sols[6])
        except (TypeError, ValueError):
            raise RuntimeError('Cannot determine axes position!')

        if 'projection' in kwargs:
            BaseAxes = SuperAxes3D
            kwargs.pop('projection')
            kwargs['auto_add_to_figure'] = False
        else:
            BaseAxes = Axes

        class SuperAxes(BaseAxes):

            def __init__(self, fig, rect=None, *args, **kwargs):
                if rect is None:
                    rect = [0.0, 0.0, 1.0, 1.0]
                super().__init__(fig, rect, *args, **kwargs)
                fig.add_axes(self)

            @property
            def x0(self):
                return self.get_position().x0

            @property
            def width(self):
                return self.get_position().width

            @property
            def y0(self):
                return 1 - (self.get_position().y0 + self.get_position().height)

            @property
            def height(self):
                return self.get_position().height

            @property
            def left(self):
                return self.x0

            @property
            def top(self):
                return self.y0

            @property
            def x1(self):
                return self.x0 + self.width

            @property
            def y1(self):
                return self.y0 + self.height

            @property
            def right(self):
                return self.x1

            @property
            def bottom(self):
                return self.y1

        ax = SuperAxes(self, [left, 1 - bottom, width, height], **kwargs)

        if style == 'modern':
            for _, sp in ax.spines.items():
                sp.set_visible(False)
            ax.patch.set_facecolor('#F0F0F0')
            ax.tick_params(axis='both', direction='in', width=0.5, length=2)
        elif style == 'blank':
            ax.axes.axis('off')
            ax.axes.set_xlim([0, 1])
            ax.axes.set_ylim([0, 1])

        return ax

    @staticmethod
    def size_hint(
        figure_width, figure_height,
        page_width=8.5, page_height=11.0,
        margin_left=0.75, margin_top=0.75
    ):

        fig = SuperFigure(figsize=(page_width, page_height), dpi=110)
        ax_letter = fig.add_axes([0, 0, 1, 1], zorder=-100)
        ax_letter.axis('off')
        ax_letter.axhline(0, ls='dashed', color='k')
        ax_letter.axhline(1, ls='dashed', color='k')
        ax_letter.axvline(0, ls='dashed', color='k')
        ax_letter.axvline(1, ls='dashed', color='k')
        ax_letter.axis([0, 1, 0, 1])

        ax_figure = fig.add_axes([
            margin_left / page_width,
            1 - (margin_top + figure_height) / page_height,
            figure_width / page_width,
            figure_height / page_height
        ])
        for _, spine in ax_figure.spines.items():
            spine.set_visible(False)
        ax_figure.set_xticks([])
        ax_figure.set_yticks([])
        ax_figure.set_facecolor((0.85, 0.85, 0.85))
