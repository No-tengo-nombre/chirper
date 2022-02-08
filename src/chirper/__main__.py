import argparse

from chirper import run_main_application, run_unit_tests, run_manual_tests


mod_desc = """
Python application to visualize and manipulate live signals.
"""

file_help = """
If specified, a file can be given for the application to inmediately
start processing live.
"""

tests_help = """
If given, the unit tests for the package will be run instead of the
main application.
"""

manual_tests_help = """
If given, the manual tests will be run. If given without any extra
arguments(i.e, simply calling `-m`) it will run all manual tests. On the
other hand, if positional arguments are given, these are considered to be
tests' names, which will be run. Example: `-m fourier1 fourier2` only runs
the tests "manual_fourier1" and "manual_fourier2".
"""

show_results_help = """
If the argument `-m` was given, the results (graphs, numerical results,
etc) of the manual tests will be shown. If given without any extra
arguments (i.e, simply calling `-s`), it shows all the tests' results.
On the other hand, if called with extra positional arguments, these are
considered to be tests' names representing the tests whose results will
be shown. Example: `-s conv1 conv2` only shows the results from the tests
"manual_conv1" and "manual_conv2".
"""


arg_parser = argparse.ArgumentParser(description=mod_desc, prog="chirper")

# Arguments for the applications IO
arg_parser.add_argument("-f", "--file", nargs=1,
                        dest="file_name", help=file_help)
arg_parser.set_defaults(file_name=None)

# Arguments for testing
arg_parser.add_argument("-t", "--tests", action="store_true",
                        dest="unit_tests", help=tests_help)
arg_parser.add_argument("-m", "--manual-tests", nargs="*", action="store",
                        dest="manual_tests", help=manual_tests_help)
arg_parser.add_argument("-s", "--show-results", nargs="*", action="store",
                        dest="show_results", help=show_results_help)
arg_parser.set_defaults(manual_tests=None, show_results=None)


###################################################################################################
#||||||||||||||||||||||||||||||||||||# Application logic #||||||||||||||||||||||||||||||||||||||||#
###################################################################################################

args = arg_parser.parse_args()

manual_tests = args.manual_tests
show_results = args.show_results
manual_not_none = manual_tests is not None
tests_are_run = manual_not_none or args.unit_tests


if tests_are_run:
    if args.unit_tests:
        run_unit_tests()
    if manual_not_none:
        run_manual_tests(manual_tests, show_results)
else:
    run_main_application(filename=args.file_name)
