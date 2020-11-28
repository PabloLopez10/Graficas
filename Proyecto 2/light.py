#Pablo Lopez
#Graficas por computadora
#14509
#Proyecto2

from utils import *

class Light(object):
    def __init__(self,color=(1,1,1), position=V3(0,0,0), intensity=1, anaglyph =False):
        self.color = color
        self.position = position
        self.intensity = intensity
        self.anaglyph = anaglyph


