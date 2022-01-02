# Chirper
## Introduction
*Chirper* is a Python package used for Digital Signal Processing. It implements different tools to create, import and export signals, as well as integral transforms and different modulation methods, useful when using signals to carry information. It also contains an application to visualize and manipulate signals in real time.

## How to install
In order to install *Chirper*, simply import it from *PyPi* by running

    pip install chirper-py

or clone this repository from *GitHub* and install it by running
    
    git clone https://github.com/No-tengo-nombre/chirper
    cd chirper
    pip install .

## How to use
### As a package
If you want to use *Chirper* as a package to manipulate signals, import the corresponding subpackages according to your purpose. As a rule of thumb, you will want to import `chirper.sgn` as it contains the base classes for all signals.

### As an application
To use *Chirper* as an application, you have to run the module with the instruction

    py -m chirper

Once you run it, a window will open that contains all the necessary configurations for you to work with signals. The basics of using the programs are:
- Select the appropiate source for what you want to do.
- Select the type of visualization you want to do.
- Configure all the necessary parameters according to your application. For this, introduce the appropiate value and press *Enter* to confirm the change.
- Once all configurations are done, start the process by turning On the source. This will start the visualization.
- When you are done, simply turn it Off. If you want to modify some parameter, you have to turn it Off in order for the modification to take effect.

The application also contains a console that allows the user to receive information about how the program is doing. There are five levels that the user can choose from:
- *DEBUG*: This shows a lot of (generally) useless information, and its intended purpose is to debug the code when something is going wrong. You generally don't want to use this level.
- *INFO*: This shows information associated to the main processes of the software, such as notifying the user when a request is sent or received. These type of notifications are more important than the ones in the *DEBUG* level, but they still usually lack importance.
- *WARNING*: This is the default level, and it contains notifications that might be important to the user (such as notifying them of an error). However, the notifications shown in this level are not critical, and are tipically derived from an user error (such as trying to set the sample rate to a string).
- *ERROR*: This level notifies the user of errors that stop the operation of the software, but are still recoverable.
- *CRITICAL*: Notifications shown in this level tipically mean the software encountered a large error that completely stops it from functioning, and so it must shut down.

Within the console is an input box that allows the user to send manual instructions to the software (currently not functional).

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
- `api` - This is an API that allows an user to send requests and receive data back from Chirper in a well formatted way. This is mainly used for the GUI that allows live signal visualization and manipulation.
- `gui` - This subpackage contains the code for the GUI that allows the user to visualize and manipulate signals in real time.

## Changing default methods
Within the `chirper` folder, there is a file `config.py`. It contains the default configurations used for the code, such as the default method used to calculate a Fourier transform, or the default method for convoluting two signals.

I want to eventually redesign this system, as it probably is very limiting. However, right now it gets the job done, so it isn't in the top of my priorities.

## Relevant links
- [Source code](https://github.com/No-tengo-nombre/chirper)
- [PyPi package](https://pypi.org/project/chirper-py/)

## License
This code is distributed under the GNU General Public License v3.0. For more information, read the [license](https://github.com/No-tengo-nombre/chirper/blob/main/LICENSE).