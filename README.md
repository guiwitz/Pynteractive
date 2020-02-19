# Pynteractive

This repository contains an example of how to use Jupyter, Matplotlib, scikit-image and Voilà to create a small interactive application. It illustrates in particular the following points:

- How to create composite color images typically used in fluorescence microscopy. This includes creating new colormaps (or LUTs) and combining them approriately. This is a quite standard procedure easily done e.g. using Fiji, but there does not seem to be an "out-of-the-box" solution for this neither in Matplotlib nor in scikit-image (but I'm happy to be proven wrong)
- How to combine an image and plot into an time-lapse animation
- How to create an interactive application allowing to do the above things

A step by step guide is given in the [image_histogram.ipynb](image_histogram.ipynb) notebook that can be run interactively by clicking on this badge [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/guiwitz/Pynteractive/master?urlpath=lab/tree/image_histogram.ipynb).

You can also directly reach the interactive application powered by Voilà by clicking on this baddge [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/guiwitz/Pynteractive/master?urlpath=%2Fvoila%2Frender%2Fimage_histogram_interactive.ipynb).



