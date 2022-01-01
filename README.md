# Chirper
## Introduction
*Chirper* is a Python package used for Digital Signal Processing. It implements different tools to create, import and export signals, as well as integral transforms and different modulation methods, useful when using signals to carry information.

## How to install
In order to install *Chirper*, simply import it from *PyPi* by running

    py -m pip install chirper-py

or clone this repository from *GitHub* and install it by running
    
    git clone https://github.com/No-tengo-nombre/chirper
    cd chirper
    pip install .

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
- `api` - This is an API that allows an user to send requests and receive data back from Chirper in a well formatted way. This is mainly used for the GUI (*not currently implemented*) that allows live signal visualization and manipulation.

## Changing default methods
Within the `chirper` folder, there is a file `config.py`. It contains the default configurations used for the code, such as the default method used to calculate a Fourier transform, or the default method for convoluting two signals.

I want to eventually redesign this system, as it probably is very limiting. However, right now it gets the job done, so it isn't in the top of my priorities.

## Relevant links
- [Source code](https://github.com/No-tengo-nombre/chirper)
- [PyPi package](https://pypi.org/project/chirper-py/)

## License
This code is distributed under the GNU General Public License v3.0. For more information, read the [license](https://github.com/No-tengo-nombre/chirper/blob/main/LICENSE).