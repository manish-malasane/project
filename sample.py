"""
This is just a sample file for basic understanding of unit testing
"""


def mul(n):
    result = 10 * n
    return result


import unittest


class TestMul(unittest.TestCase):
    def test_mul_2(self):    # when we write any test case test_ is mandatory
        result = mul(2)
        self.assertEqual(result, 20)  # assertEqual compares actual value with expected value
        self.assertNotEqual(result, [23, 34])

    def test_mul_5(self):
        result = mul(5)
        self.assertEqual(result, 50)
        self.assertNotEqual(result, [40, 70])

    def test_mul_10(self):
        result = mul(10)
        self.assertEqual(result, 100)
        self.assertNotEqual(result, [78, 45])


if __name__ == "__main__":
    unittest.main()
