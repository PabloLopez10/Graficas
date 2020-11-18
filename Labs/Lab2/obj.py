
#Pablo Lopez 
#14509
#Lab1

import struct


def color(r, g, b):
    return bytes([b, g, r])


# ===============================================================
# Loads an OBJ file
# ===============================================================


def try_int(s, base=10, val=None):
    try:
        return int(s, base)
    except ValueError:
        return val


class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()
        self.vertices = []
        self.tvertices = []
        self.normals = []
        self.vfaces = []
        self.read()

    def read(self):
        for line in self.lines:
            if line:
                try:
                    prefix, value = line.split(' ', 1)
                except:
                    prefix = ''
                if prefix == 'v':
                    self.vertices.append(list(map(float, value.split(' '))))
                if prefix == 'vt':
                    self.tvertices.append(list(map(float, value.split(' '))))
                elif prefix == 'vn':
                    self.normals.append(list(map(float, value.split(' '))))
                elif prefix == 'f':
                    self.vfaces.append([list(map(try_int, face.split('/'))) for face in value.split(' ')])


class Texture(object):
    def __init__(self, path):
        self.path = path
        self.width = 0
        self.height = 0
        self.pixels = []
        self.read()

    def read(self):
        img = open(self.path, "rb")
        print("PATH: " + str(self.path))
        img.seek(2 + 4 + 4)
        header_size = struct.unpack("=l", img.read(4))[0]
        img.seek(2 + 4 + 4 + 4 + 4)
        self.width = struct.unpack("=l", img.read(4))[0]
        self.height = struct.unpack("=l", img.read(4))[0]
        self.pixels = []
        img.seek(header_size)

        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(img.read(1))
                g = ord(img.read(1))
                r = ord(img.read(1))
                self.pixels[y].append(color(r, g, b))

        img.close()

    def get_color(self, tx, ty, intensity=1):
        x = int(tx * self.width)
        y = int(ty * self.height)
        print("GETCOLOTX: " + str(x))
        print("GETCOLOTY: " + str(y))

        # return self.pixels[y][x]
        try:
            return bytes(map(lambda b: round(b * intensity) if b * intensity > 0 else 0, self.pixels[y][x]))
        except:
            pass  # what causes this