#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib


def text(s):
    using_pgf = matplotlib.get_backend() == 'pgf'
    using_tex = matplotlib.rcParams.get('text.usetex', False)

    if using_pgf or using_tex:
        return fr'\text{{{s}}}'
    else:
        return fr'\mathdefault{{{s}}}'
