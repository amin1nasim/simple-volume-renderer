from vec3 import Vec3
from helper import * 
import math
import random

# For now we assume we have one object on the scenei
class Camera:
    def __init__(self, W=200, H=200, fov=45, position=Vec3(0, 0, 4)):
        self.W = W
        self.H = H
        self.fov = fov
        self.position = position
        
class Render:
    def __init__(self, step_size=0.02, light_dir=Vec3(0., 1.,0.), light_color=Vec3(1.3, 0.3, 0.9), backward_raymarching=True):
        self.step_size = step_size
        self.light_dir = light_dir
        self.light_color = light_color
        self.backward_raymarching = backward_raymarching

    def integrate(self, ray_orig, ray_dir, obj, bg):
        isect = obj.intersect(ray_orig, ray_dir)
        if isect['intersect'] == False:
            return bg
        
        num_samples = math.floor((isect['t1'] - isect['t0']) / self.step_size)
        if num_samples > 0:
            step_size = (isect['t1'] - isect['t0']) / num_samples
        else:
            return bg

        if self.backward_raymarching:
            result = bg
            sample_transparency = math.exp(-step_size * (obj.scattering + obj.absorption))
            for i in range(num_samples):
                t = isect['t1'] - step_size * (i + random.random())
                sample_pos = ray_orig + t * ray_dir    
                light_isect = obj.intersect(sample_pos, -1 * self.light_dir)
                light_attenuation = math.exp(-light_isect['t1'] * (obj.scattering + obj.absorption))
                result = result + self.light_color * light_attenuation *\
                        obj.phase(sample_pos, -light_dir, -ray_dir) * obj.scattering *\
                        step_size
                result = result * sample_transparency
            return result

        else:
            transparency = 1.
            result = Vec3()
            d = 5 # Rusiian roulette chance
            sample_transparency = math.exp(-step_size * (obj.scattering + obj.absorption))
            for i in range(num_samples):
                t = isect['t0'] + step_size * (i + random.random())
                sample_pos = ray_orig + t * ray_dir
                transparency *= sample_transparency
                light_isect = obj.intersect(sample_pos, -1 * self.light_dir)
                light_attenuation = math.exp(- light_isect['t1'] * (obj.scattering + obj.absorption))
                result = result + transparency * self.light_color * light_attenuation *\
                        obj.scattering * obj.phase(sample_pos, -light_dir, -ray_dir) *\
                        step_size
                # Russian roulette if we have negligible transparency left
                if transparency < 0.01:
                    if random.random() < (1/d):
                        break
                    else:
                        transparency *= d

            return bg * transparency + result

    def render(self, camera, obj, bg):
        # Generate rays
        aspectRatio = camera.W / camera.H
        focal = math.tan(math.radians(camera.fov * 0.5))
        result = []
        for j in range(camera.H):
            row = []
            for i in range(camera.W):
                x = (2 * (i + 0.5) / camera.W - 1) * focal
                y = (1 - 2 * (j + 0.5) / camera.H) * focal / aspectRatio
                z = -1.
                ray_dir = Vec3(x, y, z)
                ray_dir.normalize_()
                ray_orig = camera.position
                c = self.integrate(ray_orig, ray_dir, obj, bg)
                row.append(str(int(clip(c.x, 0, 1)*255)))
                row.append(str(int(clip(c.y, 0, 1)*255)))
                row.append(str(int(clip(c.z, 0, 1)*255)))
            result.append(row)
        
        with open('vr.ppm', 'w') as f:
            f.write("P3\n")
            f.write(f"{camera.W} {camera.H}\n")
            f.write("255\n")
            for row in result:
                f.write(' '.join(row))
                f.write('\n')
        
from objects import Sphere
#Light direction
light_dir = Vec3(0., -1., 0.)
# Light color
light_color = 14 * Vec3(1.3, 0.3, 0.9)
# Phase function
p = identity_phase_fn()
p = uniform_phase_fn()
p = greenstein_phase_fn(g=.0)
# Object
obj = Sphere(absorption=.5, scattering=0.5, phase=p)
# Camera
cam = Camera(980, 512, fov=60, position=Vec3(0, 0, 4))
# Renderer
ren = Render(step_size=0.05, light_dir=light_dir, light_color=light_color, backward_raymarching=False)
ren.render(cam, obj, bg=Vec3(0.7,0.7,0.7))
