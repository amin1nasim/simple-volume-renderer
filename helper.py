import math
import numpy as np
import unittest

def clip(value, lower, upper):
    return min(max(value, lower), upper)

def solveQuadratic(a, b, c):
    discriminant = b**2 - 4*a*c 
    if discriminant < 0:
        return (None, None)
    elif discriminant == 0:
        return (-b / (2*a), None)
    else:
        if b > 0:
            q = 0.5 * (-b - math.sqrt(discriminant))
        else:
            q = 0.5 * (-b + math.sqrt(discriminant))
        
        r1 = q / a 
        r2 = c / q
        return sorted((r1, r2))


class TestSolveQuadratic(unittest.TestCase):
    def test_zero_discr(self):
        self.assertTrue(np.isclose(solveQuadratic(9, 12, 4)[0], -2/3))
        
    def test_postive_discr(self):
        # Negative b
        self.assertTrue(np.all(np.isclose(solveQuadratic(1, -5, 6), (2, 3))))

        # Positive b
        self.assertTrue(np.all(np.isclose(solveQuadratic(-1, 5, -6), (2, 3))))

    def test_negative_discr(self):
        self.assertTrue(all([x is None for x in solveQuadratic(-10, 3, -2)]))


if __name__ == "__main__":
    unittest.main()
