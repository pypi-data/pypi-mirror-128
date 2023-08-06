#!/usr/bin/env python
# -*- coding: utf-8 -*-
from IPython import get_ipython


def mpl_setup(backend, usetex=False):
    r'''Set up Matplotlib for either the SVG or the PGF backend.

    Parameters
    ----------
    backend: 'svg' or 'pgf'
        Backend to be used. SVG for notebook inline visualization. PGF for
        LaTeX-based PDF rendering.
    usetex: bool
        Only makes a difference with the SVG backend.
        True: use TeX to handle text rendering;
        False: use MPL's own mathtext module for text rendering, which supports
        a subset TeX markup in any matplotlib text string by placing it inside
        a pair of dollar signs.
        Pro of turning on tex.usetex: wider support of LaTeX macros such as
        ``\text``.
        Cons: exact placement of text can be noticably different between SVG
        and PGF.
    '''

    if backend == 'svg':
        get_ipython().run_line_magic('matplotlib', 'inline')
        get_ipython().run_line_magic('config',
                                     "InlineBackend.figure_format = 'svg'")

    import matplotlib
    import matplotlib.font_manager as fm
    from matplotlib.font_manager import fontManager
    import fonts

    for f in fm.findSystemFonts(fontpaths=fonts.__path__):
        fontManager.addfont(f)

    matplotlib.rcParams['font.family'] = 'sans-serif'
    matplotlib.rcParams['font.weight'] = 'normal'

    # "Fonts not found" despite in fc-list: delete .cache/matplotlib
    # MPL may mistaken 'thin' fonts as 'regular', workaround:
    #     delete the 'thin' variants
    matplotlib.rcParams['font.serif'] = 'EB Garamond'
    matplotlib.rcParams['font.sans-serif'] = 'D-DIN Condensed'
    matplotlib.rcParams['font.monospace'] = 'Fira Code'

    matplotlib.rcParams['mathtext.fontset'] = 'stix'

    matplotlib.rcParams['lines.linewidth'] = 0.5

    tex_common_preamble = r"""
    \usepackage{amsmath}
    \usepackage{amstext}
    \usepackage{amssymb}
    \usepackage{euler}
    \usepackage{mathtools}
    \usepackage{amsbsy}
    \usepackage{gensymb}
    \usepackage{wasysym}
    """

    if backend == 'svg':

        if usetex:
            matplotlib.rcParams['text.usetex'] = True

        matplotlib.rcParams['text.latex.preamble'] = tex_common_preamble

    elif backend == 'pgf':

        matplotlib.use('pgf')
        matplotlib.rcParams['pgf.texsystem'] = 'xelatex'

        # Don't specify fonts in final .pgf output, leave it to compilation
        matplotlib.rcParams['pgf.rcfonts'] = False

        matplotlib.rcParams['pgf.preamble'] = tex_common_preamble + r"""
        \usepackage{fontspec}
        \setmainfont{Lora}
        \setsansfont{D-DINCondensed}
        \setmonofont{Fira Code}
        \setmathrm{D-DINCondensed}
        \setmathsf{D-DINCondensed}
        \setmathtt{Fira Code}
        \usepackage[T1]{fontenc}
        \newcommand{\tl}[2]{\textsc{\addfontfeature{LetterSpace=#1} #2}}
        """

    else:

        raise ValueError('Unknown backend "%s"' % backend)
