#Pablo Lopez   
#Graficas
#14509
#RT2

from utils import *
from sphere import Sphere
from math import pi, tan
from material import Material


BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)
RED = Color(255, 0, 0)
LIGHTBLUE = Color(100, 130, 200)
RED = Color(240, 50, 40)
BROWN = Color(165, 42, 42)
BROWN2 = Color(245, 180, 150)
GREEN = Color(0, 128, 0)

white1 = Material(diffuse = WHITE, albedo = (0.9, 0.9, 0.1), spec = 10)
white2 = Material(diffuse = WHITE, albedo = (0.65, 0.8, 0.1), spec = 15)
brown1 = Material(diffuse = BROWN, albedo = (0.4, 0.5, 0.1), spec = 10)
brown2 = Material(diffuse = BROWN2, albedo= (0.92, 0.82, 0.1), spec=30)
black = Material(diffuse = BLACK, albedo = (0.6, 0.3, 0.1), spec = 5)
red = Material(diffuse = RED, albedo = (0.6, 0.5, 0.1), spec = 5)
green = Material(diffuse = GREEN, albedo = (0.6, 0.5, 0.1), spec = 5)

class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.scene = []
        self.currentColor = LIGHTBLUE
        self.clear()

    def clear(self):
        self.pixels = [
            [self.currentColor for x in range(self.width)]
            for y in range(self.height)
        ]

    def end(self, filename='RT2.bmp'):
        self.render()
        writebmp(filename, self.width, self.height, self.pixels)

    def point(self, x, y, selectColor=None):
        try:
            self.pixels[y][x] = selectColor or self.currentColor
        except:
            pass

    def sceneIntersect(self, origin, direction):
        zbuffer = float('inf')
        
        material = None
        intersect = None
        
        for obj in self.scene:
            hit = obj.rayIntersect(origin, direction)
            if hit is not None:
                if hit.distance < zbuffer:
                    zbuffer = hit.distance
                    material = obj.material
                    intersect = hit
        return material, intersect

    def castRay(self, origin, direction):
        material, intersect = self.sceneIntersect(origin, direction)
        
        if material is None:
            return self.currentColor

        lightDir = norm(sub(self.light.position, intersect.point))
        lightDistance = length(sub(self.light.position, intersect.point))
        
        offsetNormal = mul(intersect.normal, 1.1)
        shadowOrigin = sub(intersect.point, offsetNormal) if dot(lightDir, intersect.normal) < 0 else sum(intersect.point, offsetNormal)
        shadowMaterial, shadowIntersect = self.sceneIntersect(shadowOrigin, lightDir)
        shadowIntensity = 0

        if shadowMaterial and length(sub(shadowIntersect.point, shadowOrigin)) < lightDistance:
            shadowIntensity = 0.9

        intensity = self.light.intensity * max(0, dot(lightDir, intersect.normal)) * (1 - shadowIntensity)

        reflection = reflect(lightDir, intersect.normal)
        specularIntensity = self.light.intensity * (
            max(0, -dot(reflection, direction)) ** material.spec
        )

        diffuse = material.diffuse * intensity * material.albedo[0]
        specular = Color(255, 255, 255) * specularIntensity * material.albedo[1]
        return diffuse + specular


    def render(self):
        fov = int(pi / 2) # field of view
        for y in range(self.height):
            for x in range(self.width):
                i = (2 * (x + 0.5) / self.width - 1) * self.width / self.height * tan(fov / 2)
                j = (2 * (y + 0.5) / self.height - 1) * tan(fov / 2)
                direction = norm(V3(i, j, -1))
                self.pixels[y][x] = self.castRay(V3(0, 0, 0), direction)


r = Raytracer(1000, 1000)
r.light = Light(
    position = V3(0, 0, 20),
    intensity = 1.5
)
r.scene = [
    #Oso1 
    Sphere(V3(-3, 2, -11), 1.4, white1), #cabeza blanca  
    Sphere(V3(-2.8, -1.65, -11), 2.3, white2), #cuerpo blanca
    Sphere(V3(-4.3, 3.2, -10.5), 0.5, white1), #oreja blanca
    Sphere(V3(-1.7, 3.2, -10.5), 0.5, white1), #oreja blanca
    Sphere(V3(-2.5, 1.5, -9), 0.25, white2), #nariz blanca
    Sphere(V3(-4.7, 0.22, -10.5), 0.45, white1), #brazo blanco
    Sphere(V3(-0.8, 0.23, -10.5), 0.45, white1), #brazo blanco
    Sphere(V3(-4.7, -3.6, -10.5), 0.45, white1), #pierna blanco
    Sphere(V3(-0.9, -3.5, -10.5), 0.45, white1), #pierna blanco
    Sphere(V3(-2.5, 1.8, -8), 0.1, black), #ojo
    Sphere(V3(-2, 1.8, -8), 0.1, black), #ojo
    Sphere(V3(-2.25, 1.35, -8), 0.1, black), #ojo
    Sphere(V3(-2.5, 0, -9), 0.23, red), #adorno rojo
    Sphere(V3(-2.8, -0.2, -9), 0.23, red), #adorno rojo
    Sphere(V3(-2.0, 0, -9), 0.23, red), #adorno rojo
    Sphere(V3(-2.3, -0.2, -9), 0.23, red), #adorno rojo

    #Oso2
    Sphere(V3(3, 2, -11), 1.4, brown2), #cabeza cafe
    Sphere(V3(2.8, -1.65, -11), 2.3, brown1), #cuerpo cafe 2
    Sphere(V3(4.3, 3.2, -10.5), 0.5, brown1), #oreja cafe 2
    Sphere(V3(1.7, 3.2, -10.5), 0.5, brown1), #oreja cafe 2
    Sphere(V3(2.5, 1.5, -9), 0.25,  brown1), #nariz cafe 2
    Sphere(V3(4.7, 0.22, -10.5), 0.45, brown2), #brazo cafe
    Sphere(V3(0.8, 0.23, -10.5), 0.45, brown2), #brazo cafe
    Sphere(V3(4.7, -3.6, -10.5), 0.45, brown2), #pierna cafe
    Sphere(V3(0.9, -3.5, -10.5), 0.45, brown2), #pierna cafe
    Sphere(V3(2.5, 1.8, -8), 0.1, black), #ojo
    Sphere(V3(2, 1.8, -8), 0.1, black), #ojo
    Sphere(V3(2.25, 1.35, -8), 0.1, black), #ojo
    Sphere(V3(2.5, 0, -9), 0.23, green), #adorno verde
    Sphere(V3(2.8, -0.2, -9), 0.23, green), # adorno verde
    Sphere(V3(2.0, 0, -9), 0.23, green), # adorno verde
    Sphere(V3(2.3, -0.2, -9), 0.23, green), #adorno verde
]
r.end()

