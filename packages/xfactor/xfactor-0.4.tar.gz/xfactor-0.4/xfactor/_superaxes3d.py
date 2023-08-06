#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


class SuperAxes3D(Axes3D):

    def set_scale(self, zoom=(1.0, 1.0, 1.0), pan=(0.0, 0.0, 0.0)):
        if hasattr(self, '_old_get_proj'):
            self.get_proj = self._old_get_proj

        self._old_get_proj = self.get_proj

        def get_proj():
            x, y, z = zoom
            u, v, w = pan
            T = np.array([
                [x, 0, 0, u],
                [0, y, 0, -v],
                [0, 0, z, w],
                [0, 0, 0, 1],
            ], dtype=np.float64)
            return T @ self._old_get_proj()

        self.get_proj = get_proj
