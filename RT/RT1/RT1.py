#Pablo Lopez   
#Graficas
#14509
#RT1

from utils import writebmp, norm, V3, color
from sphere import Sphere
from math import pi, tan
from material import Material

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)
BLUE = color(60, 80, 125)
ORANGE = color(240, 60, 40)
LIGHTBLUE = color(100, 130, 200)

body = Material(diffuse = color(240,240,240))
button = Material(diffuse = BLACK)
eye = Material(diffuse = WHITE)
nose = Material(diffuse = ORANGE)
lightblue = Material(diffuse = LIGHTBLUE) 

class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.scene = []
        self.currentColor = BLUE
        self.clear()

    def clear(self):
        self.pixels = [
            [self.currentColor for x in range(self.width)]
            for y in range(self.height)
        ]

    def end(self, filename='out.bmp'):
        self.render()
        writebmp(filename, self.width, self.height, self.pixels)

    def point(self, x, y, selectColor=None):
        try:
            self.pixels[y][x] = selectColor or self.currentColor
        except:
            pass

    def sceneIntersect(self, origin, direction):
        for obj in self.scene:
            if obj.ray_intersect(origin, direction):
                return obj.material
        return None

    def castRay(self, origin, direction):
        impactedMaterial = self.sceneIntersect(origin, direction)
        if impactedMaterial:
            return impactedMaterial.diffuse
        else:
            return self.currentColor

    def render(self):
        fov = int(pi / 2) # field of view
        for y in range(self.height):
            for x in range(self.width):
                i = (2 * (x + 0.5) / self.width - 1) * self.width / self.height * tan(fov / 2)
                j = (1 - 2 * (y + 0.5) / self.height) * tan(fov / 2)
                direction = norm(V3(i, j, -1))
                self.pixels[y][x] = self.castRay(V3(0, 0, 0), direction)

r = Raytracer(800, 800)
r.scene = [
    Sphere(V3(0.7, -5.05, -15), 0.25, button),
    Sphere(V3(-0.8, -5.05, -15), 0.25, button),
    Sphere(V3(0.75, -5, -15), 0.45, eye),
    Sphere(V3(-0.75, -5, -15), 0.45, eye),
    Sphere(V3(0, -4.3, -15), 0.35, nose),
    Sphere(V3(-1, -3.8, -15), 0.25, button),
    Sphere(V3(-0.4, -3.3, -15), 0.25, button),
    Sphere(V3(0.4, -3.3, -15), 0.25, button),
    Sphere(V3(1, -3.8, -15), 0.25, button),
    Sphere(V3(0, -2.0, -15), 0.45, button),
    Sphere(V3(0, 0.45, -15), 0.7, button),
    Sphere(V3(0, 3.2, -15), 0.95, button),
    Sphere(V3(0, -3.5, -12), 1.5, body),
    Sphere(V3(0, -1, -12), 2, body),
    Sphere(V3(0, 2.5, -12), 2.5, body),
]
r.end()