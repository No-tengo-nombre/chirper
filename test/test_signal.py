from signal.signal import Signal

import unittest


class TestSignal(unittest.TestCase):
    def setUp(self):
        self.signal1 = Signal(
            [i for i in range(100)],
            [i ** 2 for i in range(100)]
        )
        self.signal2 = Signal.from_function(
            [i for i in range(100)],
            lambda x: x ** 2
        )
        self.signal3 = Signal(
            [i for i in range(100)],
            [100 for _ in range(100)]
        )
        self.signal4 = Signal(
            [2 * i for i in range(50)],
            [100 for _ in range(50)]
        )
        self.signal5 = Signal.from_function(
            [2 * i for i in range(50)],
            lambda x: 100 + x - x
        )
        self.signal6 = Signal.from_function(
            [i for i in range(100)],
            lambda x: 200 + x - x
        )
        self.signal7 = Signal.from_function(
            [i for i in range(100)],
            lambda x: (x - 50) ** 3
        )
        self.signal8 = Signal.from_function(
            [1.5 * i for i in range(100)],
            lambda x: x ** 3
        )

    def test_creation(self):
        self.assertEqual(self.signal1, self.signal2, "Signal creation test failed")

    def test_indexing(self):
        self.assertEqual(45 ** 3, self.signal8[45], "Signal indexing test failed")
        for t in self.signal8.time:
            self.assertEqual(t ** 3, self.signal8[t], "Signal indexing test failed")

    def test_addition(self):
        exp_signal = Signal.from_function(
            [i for i in range(100)],
            lambda x: 2 * (x ** 2)
        )
        real_signal = self.signal1 + self.signal2
        self.assertEqual(exp_signal, real_signal, "Signal addition test failed")

    def test_subtraction(self):
        exp_signal1 = Signal.from_function(
            [i for i in range(100)],
            lambda x: x - x
        )
        exp_signal2 = Signal.from_function(
            [i for i in range(100)],
            lambda x: (x ** 2) - 100
        )
        self.assertEqual(exp_signal1, self.signal1 - self.signal2, "Signal subtraction test failed")
        self.assertEqual(exp_signal2, self.signal1 - self.signal3, "Signal subtraction test failed")

    def test_multiplication(self):
        exp_signal = Signal.from_function(
            [i for i in range(100)],
            lambda x: x ** 4
        )
        real_signal = self.signal1 * self.signal2
        self.assertEqual(exp_signal, real_signal, "Signal multiplication test failed")

    def test_division(self):
        exp_signal1 = Signal.from_function(
            [i for i in range(1, 100)],
            lambda x: x / x
        )
        exp_signal2 = Signal.from_function(
            [i for i in range(100)],
            lambda x: (x ** 2) / 100
        )
        real_signal1 = self.signal1[1:] / self.signal2[1:]
        real_signal2 = (self.signal1 / self.signal2)[1:]
        self.assertEqual(exp_signal1, real_signal1, "Signal division test failed")
        self.assertEqual(exp_signal1, real_signal2, "Signal division test failed")
        self.assertEqual(exp_signal2, self.signal1 / self.signal3, "Signal division test failed")

    def test_equality(self):
        self.assertEqual(self.signal1, self.signal1, "Signal equality test failed")
        self.assertEqual(self.signal2, self.signal2, "Signal equality test failed")

    def test_abs(self):
        exp_signal = Signal.from_function(
            [i for i in range(100)],
            lambda x: abs((x - 50) ** 3)
        )
        self.assertEqual(self.signal1, abs(self.signal1), "Signal absolute value test failed")
        self.assertEqual(exp_signal, abs(self.signal7), "Signal absolute value test failed")

    def test_interpolation(self):
        self.assertEqual(self.signal6, self.signal3 + self.signal4, "Signal interpolation test failed")
        self.assertEqual(self.signal6, self.signal3 + self.signal5, "Signal interpolation test failed")


if __name__ == '__main__':
    unittest.main()
