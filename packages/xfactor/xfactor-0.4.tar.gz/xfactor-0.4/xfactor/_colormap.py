#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Colormap, ListedColormap
from colorsys import hls_to_rgb, rgb_to_hls


def colormap_apply(cmap, f, mode='hls', clamp=True):
    '''
    Parameters
    ----------
    mode: 'rgb' or 'rgba' or 'hls' or 'hlsa'
    '''
    if not isinstance(cmap, Colormap):
        cmap = plt.cm.get_cmap(name=cmap)
    new_colors = []
    for R, G, B, A in cmap(np.arange(cmap.N)):
        if mode in ['hls', 'hlsa']:
            if mode == 'hls':
                H, L, S = f(*rgb_to_hls(R, G, B))
            elif mode == 'hlsa':
                H, L, S, A = f(*rgb_to_hls(R, G, B), A)
            if clamp:
                H = max(0.0, min(1.0, H))
                L = max(0.0, min(1.0, L))
                S = max(0.0, min(1.0, S))
            R, G, B = hls_to_rgb(H, L, S)
        elif mode in ['rgb', 'rgba']:
            if mode == 'rgb':
                R, G, B = f(R, G, B)
            elif mode == 'rgba':
                R, G, B, A = f(R, G, B, A)
            if clamp:
                R = max(0.0, min(1.0, R))
                G = max(0.0, min(1.0, G))
                B = max(0.0, min(1.0, B))
        new_colors.append((R, G, B, A))
    return ListedColormap(new_colors)
