#Pablo Lopez 
#14509
#SR1
 
import struct

def char(c):
  return struct.pack('=c', c.encode('ascii'))

def word(w):
  return struct.pack('=h', w)

def dword(d):
  return struct.pack('=l', d)

def color(r, g, b):
  return bytes([b, g, r])

# Colors
WHITE = color(255, 255, 255)
BLUE = color(0, 0, 255)

# Window
width = 0
height = 0

# Viewport
vpx = 0
vpy = 0
vpwidth = 0
vpheight = 0

# Vertex
vx1 = 0
vy1 = 0

def glInit():
  global r
  r = None

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
	r.clear(WHITE)

def glClearColor(x, y, z):
	if((x>=0 and x<=1) and (y>=0 and y<=1) and (z>=0 and z<=1)):
		x = int(round(x*255))
		y = int(round(y*255))
		z = int(round(z*255))
		r.clear(color(x,y,z))
	else:
		pass

def glVertex(x, y):
	vx1 = round(((x + 1) * (vpwidth/2)) + vpx)
	vy1 = round(((y + 1) * (vpheight/2)) + vpy)
	r.point(vx1, vy1, color(255, 255, 255))

def glColor(x, y, z):
	if((x>=0 and x<=1) and (y>=0 and y<=1) and (z>=0 and z<=1)):
		x = int(round(x*255))
		y = int(round(y*255))
		z = int(round(z*255))
		r.point(vx1, vy1, color(x, y, z))
	else:
		pass

def glFinish():
	r.write('point.bmp')

class Render(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.pixels = []
    self.clear(WHITE)

  def clear(self, color):
    self.pixels = [
      [color for x in range(self.width)] 
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

glInit()
glCreateWindow(2000, 2000)
glViewPort(800, 800, 2000, 2000)
glClear()
glClearColor(0,0,0)
glVertex(0,0)
glColor(0.9,0.5,0.1)
glFinish()