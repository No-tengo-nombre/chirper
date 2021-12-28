# SignPy
## Introduction
*SignPy* is a Python package used for Digital Signal Processing. It implements different tools to create, import and export signals, as well as integral transforms and different modulation methods, useful when using signals to carry information.

## How to install
In order to install *SignPy*, simply import it from *PyPi* by running

    py -m pip install signpy2

## Contained subpackages
Currently, the implemented subpackages are:
- `modulation` - Contains methods used for signal modulation. Right now, it allows for AM, FM and PM.
- `sgn` - Contains the code that allows the user to create signals in different ways, as well as importing and exporting them from files. As of now, both one dimensional signals (such as audio signals) and two dimensional signals (such as images) are implemented, and there are plans to implement three dimensional signals (such as videos).
- `transforms` - Contains different integral transforms which can be applied to signals. The ones currently implemented and the signals they can be applied to are:
  - `fourier`: Fourier transform (1D, 2D).
  - `ifourier`: Inverse Fourier transform (1D, 2D).
  - `hilbert`: Hilbert transform (1D).
  - `cosine`: Cosine transform (1D, 2D).
  - `sine`: Sine transform (1D, 2D).
  - `stft`: Short-time Fourier transform (1D).

## Changing default methods
Within the `signpy`, there is a file `config.py`. It contains the default configurations used for the code, such as the default method used to calculate a Fourier transform, or the default method for convoluting two signals.

I want to eventually redesign this system, as it probably is very limiting. However, right now it gets the job done, so it isn't in the top of my priorities.

## Relevant links
- [Source code](https://github.com/No-tengo-nombre/signpy)
- [PyPi package](https://pypi.org/project/signpy/)

## License
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
