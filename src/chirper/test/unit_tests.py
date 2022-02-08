from unittest import TestSuite

from chirper.test import unit


def load_tests(loader, tests, pattern):
    suite = TestSuite()
    tests = loader.loadTestsFromModule(unit)
    suite.addTests(tests)
    return suite
