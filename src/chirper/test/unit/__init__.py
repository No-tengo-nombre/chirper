from unittest import TestSuite

from chirper.test.unit import sgn


TEST_CASES = (

)

TEST_DIRS = (
    sgn,
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
