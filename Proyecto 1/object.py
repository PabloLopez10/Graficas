#Gráficas por computadora
#Pablo Lopez 14509
#P1

import struct

def color(r, g, b):
  return bytes([b, g, r])

class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()
        self.vertices = []
        self.vfaces = []
        self.vtextures = []
        self.vnormals = []
        self.read()

    def read(self):
        for line in self.lines:
            if line:
                prefix, value = line.split(' ', 1)
                if prefix == 'v':
                    lista = []
                    for x in value.split(' '):
                        lista.append(float(x))
                    self.vertices.append(lista)

                elif prefix == 'vn':

                    lista = []

                    for x in value.split(' '):
                        lista.append(float(x))

                    self.vnormals.append(lista)

                elif prefix == 'f':
                    lista = []
                    for face in value.split(' '):
                        lista2 = []
                        for f in face.split('/'):
                            if f:
                                lista2.append(int(f))
                            else:
                                lista2.append(0)
                        lista.append(lista2)
                    self.vfaces.append(lista)

                elif prefix == 'vt':
                    lista = []
                    for face in value.split(' '):
                        lista.append(face)
                    self.vtextures.append(lista)


#(24 bit bmp)
class Texture(object):
    def __init__(self, path):
        self.path = path
        self.read()

    def read(self):
        image = open(self.path, "rb")
        image.seek(2 + 4 + 4)
        header_size = struct.unpack("=l", image.read(4))[0]
        image.seek(2 + 4 + 4 + 4 + 4)

        self.width = struct.unpack("=l", image.read(4))[0]
        self.height = struct.unpack("=l", image.read(4))[0]
        self.pixels = []
        image.seek(header_size)
        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(image.read(1))
                g = ord(image.read(1))
                r = ord(image.read(1))
                self.pixels[y].append(color(r, g, b))
        image.close()

    def get_color(self, tx, ty, intensity=1):
        x = int(tx * self.width)
        y = int(ty * self.height)
        try:
            return bytes(map(lambda b: round(b * intensity) if b * intensity > 0 else 0, self.pixels[y][x]))
        except:
            pass
