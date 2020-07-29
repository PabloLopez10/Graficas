#Pablo Lopez 
#14509
#Lab1

import struct
import math
import random
import time
import struct

def char(c):
  return struct.pack('=c', c.encode('ascii'))

def word(w):
  return struct.pack('=h', w)

def dword(d):
  return struct.pack('=l', d)

def color(r, g, b):
  return bytes([b, g, r])

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)
GREEN = color(50, 200, 50)
RED = color(200, 50, 50)
BLUE = color(50, 50, 200)


class Render(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.current_color = WHITE
    self.clear()

  def clear(self):
    self.pixels = [
      [BLACK for x in range(self.width)]
      for y in range(self.height)
    ]

  def write(self, filename):
    f = open(filename, 'bw')

    
    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(14 + 40 + self.width * self.height * 3))
    f.write(dword(0))
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
        f.write(self.pixels[x][y])

    f.close()

  def set_color(self, color):
    self.current_color = color

  def point(self, x, y, color = None):
    self.pixels[y][x] = color or self.current_color

  def line(self, start, end, color = None):
    
    x1, y1 = start
    x2, y2 = end

    dy = abs(y2 - y1)
    dx = abs(x2 - x1)
    steep = dy > dx

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dy = abs(y2 - y1)
    dx = abs(x2 - x1)

    offset = 0
    threshold = dx

    y = y1
    for x in range(x1, x2 + 1):
        if steep:
            self.point(y, x, color)
        else:
            self.point(x, y, color)

        offset += dy * 2
        if offset >= threshold:
            y += 1 if y1 < y2 else -1
            threshold += dx * 2

  def poligono(self, points, color, fill = False):
        maxY = 0
        maxX = 0
        minY = 1000
        minX = 1000
        
        for pointSet in points:
            for i in range(len(pointSet)):
                if (i < (len(pointSet) - 1)):
                    self.line(pointSet[i], pointSet[i + 1], color)
                else:
                    self.line(pointSet[i], pointSet[0], color)
                if (pointSet[i][0] > maxX):
                    maxX = pointSet[i][0]
                if (pointSet[i][1] > maxY):
                    maxY = pointSet[i][1]
                if (pointSet[i][0] < minX):
                    minX = pointSet[i][0]
                if (pointSet[i][1] < minY):
                    minY = pointSet[i][1]
        if (fill):
            for y in range(minY, maxY + 1):
                point1 = (0, 0)
                point2 = (0, 0)
                initPoint = False
                endPoint = False
                pointCounter = 0
                for x in range(minX, maxX + 1):
                    point = (self.pixels[y][x][0], self.pixels[y][x][1], self.pixels[y][x][2])
                    nextPoint = (self.pixels[y][x + 1][0], self.pixels[y][x + 1][1], self.pixels[y][x + 1][2])
                    prevPoint = (self.pixels[y][x - 1][0], self.pixels[y][x - 1][1], self.pixels[y][x - 1][2])

                    if ((point == (255, 255, 255)) and (not initPoint) and (nextPoint == (0, 0, 0))):
                        point1 = (x + 1, y)
                        initPoint = True
                        pointCounter += 1

                    elif ((point == (255, 255, 255)) and (not endPoint) and (nextPoint == (0, 0, 0))):
                        point2 = (x - 1, y)
                        endPoint = True
                        pointCounter += 1

                    if (initPoint and endPoint):
                        initPoint = False
                        endPoint = False
                        
                        self.line(point1, point2, color)
                       

poligono1 = [
    (165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360),
    (250, 380), (220, 385), (205, 410), (193, 383)
]

poligono2 = [
    (321, 335), (288, 286), (339, 251), (374, 302)
]

poligono3 = [
    (377, 249), (411, 197), (436, 249)
]

poligono4 = [
    (413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37),
    (660, 52), (750, 145), (761, 179), (672, 192), (659, 214), (615, 214),
    (632, 230), (580, 230), (597, 215), (552, 214), (517, 144), (466, 180)
    ]

poligono5 = [
    (682, 175), (708, 120), (735, 148), (739, 170)
]

r = Render(800, 800)
r.poligono([poligono1], WHITE, True)
r.poligono([poligono2], WHITE, True)
r.poligono([poligono3], WHITE, True)
r.poligono([poligono4], WHITE, True)
r.poligono([poligono5], WHITE, True)
r.write('Poligonos.bmp')

