#Pablo Lopez
#Graficas por computadora
#14509
#Proyecto2

from utils import *
from light import Light
from figures import *
import struct
import math
from math import *
import random


MAX_RECURSION_DEPTH = 3
AMBIENT_LIGHT = 0.2

class Render(object):
    def __init__(self, width, height, vpw, vph, vpx, vpy):
        self.width = width
        self.height = height
        self.framebuffer = []
        self.framebuffer_int = []
        self.clearColor = (0.61,0.85,0.944)
        self.glCreateWindow()
        self.glViewport(vpw, vph, vpx, vpy)
        self.drawColor = color(0,0,0)
        self.drawColor_int = (0,0,0)
        self.glClear()
        self.scene = []

    def glInit(self):
        pass
    
    def glCreateWindow(self):
        self.framebuffer = [
            [color(158,220,240) for x in range(self.width)]
             for y in range(self.height)
        ]
        self.framebuffer_int = [
            [(158,220,240) for x in range(self.width)]
             for y in range(self.height)
        ]
    
    def glViewport(self, width, height, x, y):
        self.ViewportWidth = width
        self.ViewportHeight = height
        self.xNorm = x
        self.yNorm = y


    def glClear(self):
        self.framebuffer = [
            [color(1, 87, 155) for x in range(self.width)]
             for y in range(self.height)
        ]

    def glClearColor(self, r,g,b):
        self.clearColor = color(int(r*255),int(g*255),int(b*255))

    def glColor(self, r,g,b):
        self.drawColor = color(int(r*255),int(g*255),int(b*255))
        self.drawColor_int = (r,g,b)

    def point(self,x,y):
        self.framebuffer[x][y] = self.drawColor
        self.framebuffer_int[x][y] = self.drawColor_int

    def glVertex(self, x,y): 
        xW = int(((x+1)*(self.ViewportWidth/2))+self.xNorm)
        yW = int(((y+1)*(self.ViewportHeight/2))+self.yNorm)
        xW = (xW - 1) if xW == self.width else xW
        yW = (yW - 1) if yW == self.height else yW
        self.point(xW, yW)

    def glFinish(self, filename):
        self.render()
        f = open(filename, 'bw')
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + (self.width * self.height * 3)))
        f.write(word(0))
        f.write(word(0))
        f.write(dword(14 + 40))
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[y][x])
        f.close()

    def scene_intersect(self, orig, direction):
        zbuffer = float('inf')
        material = None
        for obj in self.scene:
            intersect = obj.ray_intersect(orig, direction)
            if intersect is not None:
                if intersect.distance < zbuffer:
                    zbuffer = intersect.distance
                    material = obj.material
                    return True, material, intersect
        return False, None, intersect
        
    def cast_ray(self, orig, direction, recursion = 0, removed_channel=-999, pos=(0,0)):
        collision, material , impact = self.scene_intersect(orig, direction)

        if collision or recursion >= MAX_RECURSION_DEPTH:
            colour = (material.diffuse[0], material.diffuse[1], material.diffuse[2])
            for light in self.lights:
                light_dir = norm(sub(light.position, impact.point))
                light_distance = length(sub(light.position, impact.point))

                offset_normal = mul(impact.normal, 1.1)
                if dot(light_dir, impact.normal) < 0:
                    shadow_orig = sub(impact.point, offset_normal)
                else:
                    shadow_orig = sum(impact.point, offset_normal)

                shadow_intersect, shadow_material, shadow_intersect_obj = self.scene_intersect(shadow_orig, light_dir)
                shadow_intensity = 0
                if shadow_intersect and light.anaglyph == False:
                    shadow_intensity = 0

                intensity = max(0,dot(light_dir, impact.normal)) * (1-shadow_intensity)

                reflection = reflect(light_dir, impact.normal)
                specular_intensity = light.intensity * (max(0, dot(reflection,direction))**material.spec)
                albedo = material.albedo
                colour = (colour[0]*intensity*albedo[0], colour[1]*intensity*albedo[0], colour[2]*intensity*albedo[0])
                specular = (light.color[0] * specular_intensity * material.albedo[1],light.color[1] * specular_intensity * material.albedo[1] ,light.color[2] * specular_intensity * material.albedo[1] )
                position = self.framebuffer_int[pos[0]][pos[1]]
                colour = (min(0.99, colour[0]+(colour[0]*AMBIENT_LIGHT)), min(0.99, colour[1]+(colour[1]*AMBIENT_LIGHT)),min(0.99, colour[2]+(colour[2]*AMBIENT_LIGHT)))
                if material.deg:
                    degradation = True if (random.random() < material.deg) else False
                    if degradation:
                        factor  = material.deg + (material.deg*0.1 if (random.random() < 0.5) else -material.deg*0.1)
                        colour = (min(colour[0]*factor, 1), min(colour[1]*factor, 1), min(colour[2]*factor, 1))
                self.glColor(*colour)
            return True
        else:
            self.glColor(*self.clearColor)
            return False

    def render(self):
        fov = pi/2
        for y in range(self.height):
                for x in range(self.width):
                    turn = 1
                    if turn >= 1:
                        i =  (2*(x + 0.5)/self.width - 1)*math.tan(fov/2)*self.width/self.height
                        j = -(2*(y + 0.5)/self.height - 1)*math.tan(fov/2)

                        direction = norm(V3(i, j, -1))
                        hit = self.cast_ray(V3(0,0,0), direction, removed_channel=None, pos=(x,y))
                        if hit:
                            self.point(x,y) 

r = Render(1000,1000,1000,1000, 0, 0)
r.lights = [
    Light(
    color=(1,1,1),
    position=V3(0,-2,2),
    intensity = 10,
    anaglyph=False
    )
]
cielo = Material(diffuse=(0,0.8,1), albedo=(1, 0), spec=10, deg=0.65)
grama = Material(diffuse=(0.48,0.98,0), albedo=(1, 0), spec=10, deg=0.3)
arbol = Material(diffuse=(0.48,0.98,0), albedo=(1, 0), spec=10)
sol =  Material(diffuse=(1,1,0), albedo=(1, 0), spec=10)
nube = Material(diffuse=(0.99,0.99,0.99), albedo=(1, 0), spec=10, deg=0.6)
cafe = Material(diffuse=(0.6,0.4,0.32), albedo=(1, 0), spec=10)
techo = Material(diffuse=(0.8,0.8,0.8), albedo=(1, 0), spec=10)
r.scene = [
    #SOL
    Sphere(V3(15, -25, -38), 6, material=sol),

    #NUBES
    Sphere(V3(-23, -22, -35), 3, material=nube),
    Sphere(V3(-20, -25, -35), 3, material=nube),
    Sphere(V3(-17, -22, -35), 3, material=nube),
    Sphere(V3(-14, -25, -35), 3, material=nube),
    Sphere(V3(-11, -22, -35), 3, material=nube),

    #TECHO
    Cube(((-1,6), (3,2), (-7, -8)), techo),

    #CASA
    Cube(((1.8,3.3), (4,3.5), (-7, -8)), cielo),
    Cube(((0,5), (6.5,3), (-7, -8)), cafe ),

    #ARBOL
    Sphere(V3(-20, -9.5, -35), 5, material=arbol),
    Sphere(V3(-24, -4.5, -35), 5, material=arbol),
    Sphere(V3(-17, -4.5, -35), 5, material=arbol),
    Sphere(V3(-20, 0.5, -35), 5, material=arbol),
    Sphere(V3(-27, 0.5, -35), 5, material=arbol),
    Sphere(V3(-13, 0.5, -35), 5, material=arbol),
    Cube(((-5.5,-3), (3,1), (-7, -8)), cafe ),

    #FONDO
    Cube(((-8, 8), (-0.5, 5), (-8, -2)), grama),
]
r.glFinish("proyecto2.bmp")


