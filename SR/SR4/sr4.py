#Gráficas por computadora
#Pablo Lopez 14509
#SR4

import sys
import copy
from Lib import *
from obj import *
import struct

def char(c):
    return struct.pack("=c", c.encode('ascii'))


def word(w):
    return struct.pack("=h", w)


def dword(d):
    return struct.pack("=l", d)


def color(r, g, b):
    return bytes([b, g, r])


class Bitmap(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.clearColor = color(0, 0, 0)
        self.currentColor = color(0, 0, 0)
        self.pixels = []
        self.clear()

    def clear(self):
        self.pixels = [
            [self.clearColor for x in range(self.width)]
            for y in range(self.height)
        ]

    def write(self, filename):
        f = open(filename, 'bw')

        # file header (14)
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # image header (40)
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

        # pixel data
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.pixels[x][y])
        f.close()

    def point(self, x, y, color=None):
        if color is None:
            color = self.currentColor
        if (x >= self.width or x < 0):
            x = self.width - 1

        if (y >= self.height or y < 0):
            y = self.height - 1

        self.pixels[y][x] = color


screen = None
viewPort = {"x": 0, "y": 0, "width": 0, "heigth": 0}
blue = color(0, 0, 255)
red = color(255, 0, 0)
green = color(0, 255, 0)
colorStandard = 255
vertexBuffer = []
zBuffer = []


sign = lambda a: (a > 0) - (a < 0)


def glInit():
    pass


def glCreateWindow(width, heigth):
    global screen
    screen = Bitmap(width, heigth)


def glViewPort(x, y, width, heigth):
    global viewPort, zBuffer
    viewPort["x"] = x
    viewPort["y"] = y
    viewPort["width"] = width
    viewPort["heigth"] = heigth
    zBuffer = [[-999 for x in range(0, width+ 1)] for y in range(0, heigth + 1)]


def glClear():
    screen.clear()


def glClearColor(r, g, b):
    screen.color = color(r, g, b)


# Recibe parametros entre -1 y 1
def glVertex(x, y):
    global viewPort
    global screen
    newX = int((x + 1) * (viewPort["width"] / 2) + viewPort["x"])
    newY = int((y + 1) * (viewPort["heigth"] / 2) + viewPort["y"])
    screen.point(newX, newY, screen.currentColor)


def glColor(r, g, b):
    r = int(r * colorStandard)
    g = int(g * colorStandard)
    b = int(b * colorStandard)
    screen.currentColor = color(r, g, b)


def glLine(x0, y0, x1, y1):
    global viewPort
    global screen
    x0, y0 = normalize(x0, y0, viewPort)
    x1, y1 = normalize(x1, y1, viewPort)

    # Setup initial conditions
    dx = x1 - x0
    dy = y1 - y0

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
        swapped = True

    # Recalculate differentials
    dx = x1 - x0
    dy = y1 - y0

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y0 < y1 else -1

    # Iterate over bounding box generating points between start and end
    y = y0
    points = []
    for x in range(x0, x1 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()

    for point in points:
        screen.point(point[0], point[1], screen.currentColor)


def glFinish():
    screen.write('out.bmp')


def glLoad(name, scale, translateX, translateY, translateZ):
    global screen, vertexBuffer
    model = Obj(name)
    for face in model.vfaces:
        vcount = len(face)
        for j in range(vcount):
            f1 = face[j][0]
            v1 = copy.copy(model.vertices[f1 - 1])
            # v1 = [(x * scale) + translateX for x in v1]
            v1[0] = (v1[0] * scale) + translateX
            v1[1] = (v1[1] * scale) + translateY
            v1[2] = (v1[2] * scale) + translateZ
            vertexBuffer.append(v1)
    vertexBuffer = iter(vertexBuffer)

def length(v0):
  return (v0[0]**2 + v0[1]**2 + v0[2]**2)**0.5

def norm(v0):
    v0length = length(v0)

    if not v0length:
        return [0, 0, 0]

    return [v0[0] / v0length,
            v0[1] / v0length,
            v0[2] / v0length]

def cross(v1, v2):
    return [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    ]

def dot(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

def barycentric(A, B, C, P):
    v1 = [C[0] - A[0], B[0] - A[0], A[0] - P[0]]
    v2 = [C[1] - A[1], B[1] - A[1], A[1] - P[1]]

    b = cross(v1, v2)

    if(abs(b[2]) < 1):
        return -1, -1, -1

    return (1 - (b[0] + b[1]) / b[2], b[1] / b[2], b[0] / b[2])

def sub(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]]

def getPixels(x, y):
    global viewPort
    newX = int((x + 1) * (viewPort["width"] / 2) + viewPort["x"])
    newY = int((y + 1) * (viewPort["heigth"] / 2) + viewPort["y"])
    return newX, newY

def glTriangle():
    global vertexBuffer, viewPort, zBuffer
    A = next(vertexBuffer)
    B = next(vertexBuffer)
    C = next(vertexBuffer)
    light = [0,0,1]
    normal = norm(cross(sub(B, A), sub(C, A))) #Falta el norm
    intensity = dot(light, normal)

    minX = round(min(A[0], B[0], C[0]))
    minY = round(min(A[1], B[1], C[1]))
    maxX = round(max(A[0], B[0], C[0]))
    maxY = round(max(A[1], B[1], C[1]))

    for x in range(minX, maxX + 1):
        for y in range(minY, maxY + 1):
            w, v, u = barycentric(A, B, C, [x, y])
            if u >= 0 and v >= 0 and w >= 0:
                z = w * A[2] + v * B[2] + u * C[2]
                grey = round(255 * intensity)
                if grey < 0:
                    continue
                if 0 < x < viewPort["width"] and  0 < y < viewPort["heigth"] and zBuffer[y][x] < z:
                    screen.point(x, y, color(grey, grey, grey))
                    zBuffer[y][x] = z
            #algoritmo para cambiar color del punto dependiendo de la direccion de la luz

def glDraw():
    while True:
        try:
            glTriangle()
        except StopIteration:
            break

glInit()
glCreateWindow(1000, 1000)
glViewPort(0, 0, 1000, 1000)
glClearColor(1, 1, 1)
glClear()
glColor(1, 1, 1)
glLoad("PenguinBaseMesh.obj", 700, 500, 100, 0)
glDraw()
glFinish()