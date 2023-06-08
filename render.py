from vec3 import Vec3
from helper import clip
import math

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
        transparency = 1.

        if self.backward_raymarching:
            result = bg
            for i in range(num_samples):
                t = isect['t1'] - self.step_size * (i + 0.5)
                sample_pos = ray_orig + t * ray_dir
                
                sample_transparency = math.exp(-self.step_size * obj.absorption)
                light_isect = obj.intersect(sample_pos, -1 * self.light_dir)
                light_attenuation = math.exp(- light_isect['t1'] * obj.absorption)
                result = result + self.light_color * obj.scattering * light_attenuation * self.step_size
                result = result * sample_transparency
            return result
        else:
            transparency = 1.
            result = Vec3()
            for i in range(num_samples):
                t = isect['t0'] + self.step_size * (i + 0.5)
                sample_pos = ray_orig + t * ray_dir
                sample_transparency = math.exp(-self.step_size * obj.absorption)
                transparency *= sample_transparency
                light_isect = obj.intersect(sample_pos, -1 * self.light_dir)
                light_attenuation = math.exp(- light_isect['t1'] * obj.absorption)
                result = result + transparency * self.light_color * obj.scattering * light_attenuation * self.step_size

            return bg * transparency + result
    
    def render(self, camera, obj, bg):
        # Generate rays
        aspectRatio = camera.W / camera.H
        focal = math.tan(math.radians(camera.fov * 0.5))
        result = []
        for j in range(camera.H):
            for i in range(camera.W):
                x = (2 * (i + 0.5) / camera.W - 1) * focal
                y = (1 - 2 * (j + 0.5) / camera.H) * focal / aspectRatio
                z = -1.
                ray_dir = Vec3(x, y, z)
                ray_dir.normalize_()
                ray_orig = camera.position
                c = self.integrate(ray_orig, ray_dir, obj, bg)
                result.append(str(int(clip(c.x, 0, 1)*255)))
                result.append(str(int(clip(c.y, 0, 1)*255)))
                result.append(str(int(clip(c.z, 0, 1)*255)))

        with open('vr.ppm', 'w') as f:
            f.write("P3\n")
            f.write(f"{camera.W} {camera.H}\n")
            f.write("255\n")
            f.write(' '.join(result))



from objects import Sphere

obj = Sphere(absorption=1., scattering=0.6)
cam = Camera(980, 512, fov=60)
ren = Render(step_size=0.02, backward_raymarching=True)
ren.render(cam, obj, Vec3(0.7,0.7,0.7))
