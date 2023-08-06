#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._setup import mpl_setup
from ._superfigure import SuperFigure
from ._superaxes3d import SuperAxes3D
from ._colormap import colormap_apply


__version__ = '0.4'
__all__ = ['mpl_setup', 'SuperFigure', 'SuperAxes3D', 'colormap_apply']

rc = {}
