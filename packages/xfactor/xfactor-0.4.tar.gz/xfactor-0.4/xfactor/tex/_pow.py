#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from ._text import text


def pow(a, b, mathmode=False):
    t = fr'{text(a)}^{text(b)}'
    if mathmode is True:
        t = f'${t}$'
    return t
