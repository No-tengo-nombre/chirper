# SignPy
## Introduction
*SignPy* is a Python package used for Digital Signal Processing. It implements different tools to create, import and export signals, as well as integral transforms and different modulation methods, useful when using signals to carry information.

## Contained subpackages
Currently, the implemented subpackages are:
- `modulation` - Contains methods used for signal modulation. Right now, it allows for AM and PM, but FM is in the works.
- `sgn` - Contains the code that allows the user to create signals in different ways, as well as importing and exporting them from files. As of now, only one dimensional signals (such as audio signals) are implemented with the object `Signal1`, but there are plans to allow for two dimensional signals (e.g images) and even three dimensional signals (e.g videos, which consist of two spatial dimensions and a time dimension).
- `transforms` - Contains different integral transforms which can be applied to signals. The ones currently implemented are:
  - `fourier`: Fourier transform.
  - `ifourier`: Inverse Fourier transform.
  - `hilbert`: Hilbert transform.

## Changing default methods
Within the `signpy`, there is a file `config.py`. It contains the default configurations used for the code, such as the default method used to calculate a Fourier transform, or the default method for convoluting two signals.

I want to eventually redesign this system, as it probably is very limiting. However, right now it gets the job done, so it isn't in the top of my priorities.

# License
MIT License

Copyright (c) 2021 Cristóbal Allendes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
