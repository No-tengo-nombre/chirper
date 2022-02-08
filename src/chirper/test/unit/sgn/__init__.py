from unittest import TestSuite

from chirper.test.unit.sgn.test_signal import TestSignal


TEST_CASES = (
    TestSignal,
)

TEST_DIRS = (

)


def load_tests(loader, tests, pattern):
    suite = TestSuite()
    for test_class in TEST_CASES:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    for test_dir in TEST_DIRS:
        tests = loader.loadTestsFromModule(test_dir)
        suite.addTests(tests)
    return suite
