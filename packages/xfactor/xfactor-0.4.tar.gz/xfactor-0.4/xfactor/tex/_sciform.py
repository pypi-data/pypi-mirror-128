#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from ._pow import pow
from ._text import text


def sciform(f, frac_digits=1, exp_digits=1, mathmode=False):
    exp = int(np.floor(np.log10(f)))
    man = f / 10**exp
    t = r'{man}\!\!\times\!\!{exp10}'.format(
        man=text(f'%.{frac_digits}f' % man),
        exp10=pow(
            10,
            f'%0{exp_digits}d' % exp,
            mathmode=False
        )
    )
    if mathmode is True:
        t = f'${t}$'
    return t
