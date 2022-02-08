from tqdm import tqdm

from chirper.test.manual import *


AVAILABLE_TESTS = {
    "interp1": manual_interp1,
    "conv1": manual_conv1,
    "conv2": manual_conv2,
    "io1": manual_io1,
    "io2": manual_io2,
    "hilbert": manual_hilbert,
    "cos1": manual_cos1,
    "cos2": manual_cos2,
    "sin1": manual_sin1,
    "fourier1": manual_fourier1,
    "fourier2": manual_fourier2,
    "spectr": manual_spectr,
    "modulation": manual_modulation,
    "am_modulation": manual_am_modulation,
}

SHOW_TESTS = {
    "interp1": False,
    "conv1": False,
    "conv2": False,
    "io1": False,
    "io2": False,
    "hilbert": False,
    "cos1": False,
    "cos2": False,
    "sin1": False,
    "fourier1": False,
    "fourier2": False,
    "spectr": False,
    "modulation": False,
    "am_modulation": False,
}


def _tests_to_run(tests):
    if tests == []:
        to_run = AVAILABLE_TESTS
    else:
        to_run = {}
        for key in tests:
            to_run[key] = AVAILABLE_TESTS[key]
    return to_run


def _tests_to_show(show):
    if show == []:
        show_dict = {True for _ in SHOW_TESTS}
    else:
        show_dict = SHOW_TESTS
        if show is not None:
            for key in show:
                show_dict[key] = True
    return show_dict


def run(tests, show):
    to_run = _tests_to_run(tests)
    show_dict = _tests_to_show(show)
    for key, val in tqdm(to_run.items(), desc="Running manual tests"):
        val.main(show_dict[key])
