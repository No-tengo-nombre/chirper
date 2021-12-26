import unittest

from signpy.sgn import Signal1


class TestSignal(unittest.TestCase):
    def setUp(self):
        self.signal1 = Signal1(
            [i for i in range(100)],
            [i ** 2 for i in range(100)]
        )
        self.signal2 = Signal1.from_function(
            [i for i in range(100)],
            lambda x: x ** 2
        )
        self.signal3 = Signal1(
            [i for i in range(100)],
            [100 for _ in range(100)]
        )
        self.signal4 = Signal1(
            [2 * i for i in range(50)],
            [100 for _ in range(50)]
        )
        self.signal5 = Signal1.from_function(
            [2 * i for i in range(50)],
            lambda x: 100 + x - x
        )
        self.signal6 = Signal1.from_function(
            [i for i in range(100)],
            lambda x: 200 + x - x
        )
        self.signal7 = Signal1.from_function(
            [i for i in range(100)],
            lambda x: (x - 50) ** 3
        )
        self.signal8 = Signal1.from_function(
            [1.5 * i for i in range(100)],
            lambda x: x ** 3
        )

    def test_creation(self):
        self.assertEqual(self.signal1, self.signal2,
                         "Time signal creation test failed")

    def test_indexing(self):
        self.assertEqual(
            45 ** 3, self.signal8(45), "Continous time signal indexing test failed")
        for t in self.signal8.axis:
            self.assertEqual(
                t ** 3, self.signal8(t), "Continous time signal indexing test failed")

    def test_addition(self):
        exp_signal = Signal1.from_function(
            [i for i in range(100)],
            lambda x: 2 * (x ** 2)
        )
        real_signal = self.signal1 + self.signal2
        self.assertEqual(exp_signal, real_signal,
                         "Time signal addition test failed")

    def test_subtraction(self):
        exp_signal1 = Signal1.from_function(
            [i for i in range(100)],
            lambda x: x - x
        )
        exp_signal2 = Signal1.from_function(
            [i for i in range(100)],
            lambda x: (x ** 2) - 100
        )
        self.assertEqual(exp_signal1, self.signal1 - self.signal2,
                         "Time signal subtraction test failed")
        self.assertEqual(exp_signal2, self.signal1 - self.signal3,
                         "Time signal subtraction test failed")

    def test_multiplication(self):
        exp_signal = Signal1.from_function(
            [i for i in range(100)],
            lambda x: x ** 4
        )
        real_signal = self.signal1 * self.signal2
        self.assertEqual(exp_signal, real_signal,
                         "Time signal multiplication test failed")

    def test_division(self):
        exp_signal1 = Signal1.from_function(
            [i for i in range(1, 100)],
            lambda x: x / x
        )
        exp_signal2 = Signal1.from_function(
            [i for i in range(100)],
            lambda x: (x ** 2) / 100
        )
        sign1_cut = Signal1(self.signal1.axis[1:], self.signal1.values[1:])
        sign2_cut = Signal1(self.signal2.axis[1:], self.signal2.values[1:])
        div = (self.signal1 / self.signal2)

        real_signal1 = sign1_cut / sign2_cut
        real_signal2 = Signal1(div.axis[1:], div.values[1:])
        self.assertEqual(exp_signal1, real_signal1,
                         "Time signal division test failed")
        self.assertEqual(exp_signal1, real_signal2,
                         "Time signal division test failed")
        self.assertEqual(exp_signal2, self.signal1 /
                         self.signal3, "Time signal division test failed")

    def test_equality(self):
        self.assertEqual(self.signal1, self.signal1,
                         "Time signal equality test failed")
        self.assertEqual(self.signal2, self.signal2,
                         "Time signal equality test failed")

    def test_abs(self):
        exp_signal = Signal1.from_function(
            [i for i in range(100)],
            lambda x: abs((x - 50) ** 3)
        )
        self.assertEqual(self.signal1, abs(self.signal1),
                         "Time signal absolute value test failed")
        self.assertEqual(exp_signal, abs(self.signal7),
                         "Time signal absolute value test failed")


if __name__ == '__main__':
    unittest.main()
