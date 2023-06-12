from abc import ABC, abstractmethod
from helper import solveQuadratic
import helper
from vec3 import Vec3
import unittest
import numpy as np

class Object(ABC):
    def __init__(self, type_, color_):
        self.type = type_
        if isinstance(color_, Vec3):
            self.color = color_
        else:
            self.color = Vec3(*color_)

    @abstractmethod
    def intersect(self, rayOrig, rayDir):
        pass

class Sphere(Object):
    def __init__(self, c=Vec3(0,0,0), r=1, color=(0,0,0), absorption=0.1, scattering=0.1, phase=helper.uniform_phase_fn()):
        super().__init__(type_=1, color_=color)
        self.center = c
        self.radius = r
        self.absorption = absorption
        self.scattering = scattering
        self.phase = phase

    def intersect(self, rayOrig, rayDir):
        if (rayDir.length() - 1. > 1e-5):
            rayDir.normalize_()
        OC = rayOrig - self.center 
        a = 1.
        b = 2 * (OC).dot(rayDir)
        c = OC.dot(OC) - self.radius**2

        sol = solveQuadratic(a, b, c)

        # If the ray doesn't intersect or is tangent
        if any(elm is None for elm in sol):
            return {'intersect':False}

        # If the object is entirely behind the camera        
        if all(elm<=0 for elm in sol):
            return {'intersect':False}

        # If both answers are not negative then at least the bigger one (t1) is positve.
        # If t0 is nagative then the camera is inside the object
        return {'intersect':True, 't0':sol[0] if sol[0]>0. else 0., 't1':sol[1]}


    def __repr__(self):
        return f'Shpere: center={self.center} radius={self.radius} color={self.color}' 


class TestSphere(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sphere = Sphere(c=Vec3(-5, 0, 1))

    def test_intersect(self):
        # Two intersections
        rayOrig = Vec3(5, 0, 1)
        rayDir = Vec3(-1, 0, 0).normalize()
        insec = TestSphere.sphere.intersect(rayOrig, rayDir)
        self.assertTrue(insec['intersect']==True)
        self.assertTrue(np.all(np.isclose((insec['t0'], insec['t1']), (9, 11))))
        # One intersection
        rayOrig = Vec3(5, 0, 2)
        insec = TestSphere.sphere.intersect(rayOrig, rayDir)
        self.assertTrue(insec['intersect']==False)
        # No intersection
        rayOrig = Vec3(5, 0, 3)
        insec = TestSphere.sphere.intersect(rayOrig, rayDir)
        self.assertTrue(insec['intersect']==False)
        # Camera inside the object
        rayOrig = Vec3(-4.5, 0, 1)
        insec = TestSphere.sphere.intersect(rayOrig, rayDir)
        self.assertTrue(insec['intersect']==True)
        self.assertTrue(np.all(np.isclose((insec['t0'], insec['t1']), (0, 1.5))))

if __name__ == "__main__":
    unittest.main()
