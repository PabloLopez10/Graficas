#Pablo Lopez 
#14509
#SR2
 
import struct
import random

def char(c):
  return struct.pack('=c', c.encode('ascii'))

def word(w):
  return struct.pack('=h', w)

def dword(d):
  return struct.pack('=l', d)

def color(r, g, b):
  return bytes([b, g, r])

WHITE = color(255, 255, 255)
BLUE = color(0, 0, 255)
width = 0
height = 0
r = None
vpx = 0
vpy = 0
vpwidth = 0
vpheight = 0
vx1 = 0
vy1 = 0

def glInit():
  	pass

def glCreateWindow(gwidth, gheight):
  	global r, width, height
  	width = gwidth
  	height = gheight
  	r = Render(width, height)

def glViewPort(x, y, width, height):
	global vpx, vpy, vpwidth, vpheight
	vpwidth = width
	vpheight = height
	vpx = x
	vpy = y

def glClear():
	r.clear(255, 255, 255)

def glClearColor(x, y, z):
	if((x>=0 and x<=1) and (y>=0 and y<=1) and (z>=0 and z<=1)):
		x = int(round(x))
		y = int(round(y))
		z = int(round(z))
		r.clear(x, y, z)
	else:
		pass

def glLine():
    r.line(0.5, 0.5, 0.75, 0.75, WHITE)

def glColor(x, y, z):
	if((x>=0 and x<=1) and (y>=0 and y<=1) and (z>=0 and z<=1)):
		x = int(round(x*255))
		y = int(round(y*255))
		z = int(round(z*255))
		r.point(vx1, vy1, color(x, y, z))
	else:
		pass

def glFinish():
	r.write('linea.bmp')

class Render(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.pixels = []
    self.clear(0, 0, 0)

  def clear(self, r, g, b):
    self.pixels = [
      [color(r,g,b) for x in range(self.width)] 
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

  def point(self, x, y, color):
  	self.pixels[x][y] = color

  def line(self, x0, y0, x1, y1, color):

    x0 = (int)(width * x0)
    x1 = (int)(width * x1)
    y0 = (int)(height * y0)
    y1 = (int)(height * y1)

    dy = abs(y1 - y0)
    dx = abs(x1 - x0)
    steep = dy > dx

    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dy = abs(y1 - y0)
    dx = abs(x1 - x0)

    offset = 0
    threshold = dx

    y = y0
    for x in range(x0, x1 + 1):
        if steep:
            self.point(x, y, color)
        else:
            self.point(y, x, color)
        
        offset += dy * 2
        if offset >= threshold:
            y += 1 if y0 < y1 else -1
            threshold += dx * 2

glInit()
glCreateWindow(800, 600)

#glClear()
#glViewPort(0, 0, 450, 450)
#glClearColor(0.2,0.8,1)
glLine()
#glColor(0.9,0.5,0.1)
glFinish()