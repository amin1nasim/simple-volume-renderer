import math
import numpy as np
import unittest

class Vec3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def get_coord(self):
        return (self.x, self.y, self.z)

    def length(self):
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

    def normalize(self):
        length = self.length()
        return Vec3(self.x/length, self.y/length, self.z/length)
    
    def normalize_(self):
        length = self.length()
        self.x = self.x/length
        self.y = self.y/length
        self.z = self.z/length

    def __add__(self, other):
        return Vec3(self.x+other.x, self.y+other.y, self.z+other.z)

    def __sub__(self, other):
        return Vec3(self.x-other.x, self.y-other.y, self.z-other.z)

    def __mul__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x*other.x, self.y*other.y, self.z*other.z)
        else:
            return Vec3(self.x*other, self.y*other, self.z*other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __matmul__(self, other):
        return self.dot(other)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def dot(self, other):
        temp = self * other
        return temp.x + temp.y + temp.z 
    
    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z})'

class TestVec3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.np_a = (np.random.rand(100, 3) - 0.5) * 100
        cls.np_b = (np.random.rand(100, 3) - 0.5) * 100

    def test_add(self):
        c = TestVec3.np_a + TestVec3.np_b
        result = [(Vec3(*x) + Vec3(*y)).get_coord()
                for x, y in zip(TestVec3.np_a,TestVec3.np_b)]
        result_np = np.array(result)
        self.assertTrue(np.all(np.isclose(result_np, c)))
	
    def test_sub(self):
        c = TestVec3.np_a - TestVec3.np_b
        result = [(Vec3(*x) - Vec3(*y)).get_coord()
                for x, y in zip(TestVec3.np_a, TestVec3.np_b)]
        result_np = np.array(result)
        self.assertTrue(np.all(np.isclose(result_np, c)))

    def test_mul(self):
        c = TestVec3.np_a * TestVec3.np_b
        result = [(Vec3(*x) * Vec3(*y)).get_coord()
                for x, y in zip(TestVec3.np_a, TestVec3.np_b)]
        result_np = np.array(result)
        self.assertTrue(np.all(np.isclose(result_np, c)))
    
    def test_dot(self):
        c = (TestVec3.np_a @ TestVec3.np_b.T).diagonal()
        result = [Vec3(*x) @ Vec3(*y)
                for x, y in zip(TestVec3.np_a, TestVec3.np_b)]
        result_np = np.array(result)
        self.assertTrue(np.all(np.isclose(result_np, c)))
    
    def test_normalize(self):
        c = TestVec3.np_a / np.linalg.norm(TestVec3.np_a, axis=1, keepdims=True)
        result = [Vec3(*x).normalize().get_coord() for x in TestVec3.np_a]
        result_np = np.array(result)
        self.assertTrue(np.all(np.isclose(result_np, c)))


if __name__ == "__main__":
    unittest.main()
