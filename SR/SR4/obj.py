class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()
        self.vertices = []
        self.vfaces = []
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