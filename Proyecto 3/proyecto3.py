#Pablo Lopez
#14509
#Graficas
#Lab4

import pygame
from math import pi, cos, sin, atan2
import time

WHITE = (255, 255, 255)

wall1 = pygame.image.load('./wall.jpg')
wall2 = pygame.image.load('./wall2.png')

gun = pygame.image.load('./gun.png')

textures = {
    "1": wall1,
    "2": wall2
}

enemies = [
  {
    "x": 320,
    "y": 420,
    "texture": pygame.image.load('./girl2.png')
  }
]

fires = [
    {
        "x":100,
        "y":200,
        "texture": pygame.image.load('./fire.jpg')
    },
    {
        "x":430,
        "y":75,
        "texture": pygame.image.load('./fire.jpg')
    }
]

class Raycaster:
    def __init__(self, screen):
        _, _, self.width, self.height = screen.get_rect()
        self.screen = screen
        self.blocksize = 50
        self.map = []

        self.player = {
            "x": self.blocksize + 25,
            "y": self.blocksize + 25,
            "a": 0,
            "fov": pi/3,
        }
        self.zbuffer = [-float("inf") for z in range(0,500)]

    def point(self, x, y, c):
        screen.set_at((int(x), int(y)), c)

    def gun(self, xi, yi, w = 256, h = 256):
        for x in range(xi, xi + w):
          for y in range(yi, yi + h):
            tx = int((x - xi) * 32/w)
            ty = int((y - yi) * 32/h)
            c = gun.get_at((tx, ty))
            if c != (152, 0, 136, 255):
              self.point(x, y, c)
    
    def draw_rectangle(self, x, y, texture):
        for cx in range(x, x + 50):
            for cy in range(y, y + 50):
                # Texture size: 128x128
                tx = int((cx - x) * 128/50)
                ty = int((cy - y) * 128/50)
                c = texture.get_at((tx, ty))
                self.point(cx, cy, c)
    
    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    def cast_ray(self, a):
        d = 0
        while True:
            x = self.player["x"] + d * cos(a)
            y = self.player["y"] + d * sin(a)

            i = int(x/self.blocksize)
            j = int(y/self.blocksize)

            if self.map[j][i] != ' ':
                hitx = x - i*50
                hity = y - j*50

                if 1 < hitx < 49:
                    maxhit = hitx
                else:
                    maxhit = hity

                tx = int(maxhit * 128/50)
                return d, self.map[j][i], tx

            self.point(x, y, (255, 255, 255))
            d += 1
    
    def draw_stake(self, x, h, tx, texture):
        start = int(250 - h/2)
        end = int(250 + h/2)
        for y in range(start, end):
            ty = int((y - start) * (128 / (end-start)))
            c = texture.get_at((tx, ty))
            self.point(x, y, c)

    def draw_sprite(self, sprite):
        sprite_a = atan2(sprite["y"] - self.player["y"], (sprite["x"] - self.player["x"]))
        sprite_d = ((self.player["x"] - sprite["x"])**2 + (self.player["y"] - sprite["y"])**2)**0.5
        sprite_size = int(500/sprite_d * 50)
        sprite_x = int(500 + (sprite_a - self.player["a"]) * 500/self.player["fov"] + 250 - sprite_size/2)
        sprite_y = int(250 - sprite_size/2)

        for x in range(sprite_x, sprite_x + sprite_size):
            for y in range(sprite_y, sprite_y + sprite_size):
                i = x - 500
                if 500 < x < 1000 and self.zbuffer[i] >= sprite_d:
                    tx = int((x - sprite_x) * 128/sprite_size)
                    ty = int((y - sprite_y) * 128/sprite_size)
                    c = sprite["texture"].get_at((tx, ty))
                    self.point(x, y, c)

    def draw_sprite2(self, sprite):
        sprite_a = atan2(sprite["y"] - self.player["y"], (sprite["x"] - self.player["x"]))
        sprite_d = ((self.player["x"] - sprite["x"])**2 + (self.player["y"] - sprite["y"])**2)**0.5
        sprite_size = int(500/sprite_d * 50)
        sprite_x = int(500 + (sprite_a - self.player["a"]) * 500/self.player["fov"] + 250 - sprite_size/2)
        sprite_y = int(250 - sprite_size/2)

        for x in range(sprite_x, sprite_x + sprite_size):
            for y in range(sprite_y, sprite_y + sprite_size):
                i = x - 500
                if 500 < x < 1000 and self.zbuffer[i] >= sprite_d:
                    tx = int((x - sprite_x) * 128/sprite_size)
                    ty = int((y - sprite_y) * 128/sprite_size)
                    c = sprite["texture"].get_at((tx, ty))
                    if c!= (255, 255, 255, 255):
                        self.point(x, y, c)

    def render(self):
        # Overhead view
        for x in range(0, 500, self.blocksize):
            for y in range(0, 500, self.blocksize):
                i = int(x/self.blocksize)
                j = int(y/self.blocksize)
                if self.map[j][i] != ' ':
                    self.draw_rectangle(x, y, textures[self.map[j][i]])
        
        self.point(self.player["x"], self.player["y"], (255, 255, 255))

        #draw first person view
        for i in range(0, 500):
            a = self.player["a"] - self.player["fov"]/2 + (i * self.player["fov"]/500)
            d, m, tx = self.cast_ray(a)

            x = 500 + i
            h = (500/(d * cos(a - self.player["a"]))) * 50
            self.zbuffer[i] = d

            self.draw_stake(x, h, tx, textures[m])

        for i in range (0, 500):
            self.point(499, i, (0, 0, 0))
            self.point(500, i, (0, 0, 0))
            self.point(501, i, (0, 0, 0))   

        for enemy in enemies:
            self.draw_sprite(enemy)

        self.gun(1000 - 256 - 128, 500 - 256)
        
        for fire in fires:
            self.draw_sprite2(fire)

    def texts(self, text, font):
        text = font.render(text, True, WHITE)
        return text, text.get_rect()

    def getFps(self):
        font = pygame.font.Font(None, 35)
        fps = "FPS: " + str(int(clock.get_fps()))
        fps = font.render(fps, 1, WHITE)
        return fps

    def menu(self):
        self.mi_music()
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        intro = False

            screen2.fill((0,0,0))
            smallText = pygame.font.Font('freesansbold.ttf', 40)
            bigText = pygame.font.Font('freesansbold.ttf', 90)
            smallerText = pygame.font.Font('freesansbold.ttf', 30)

            text, textRect = self.texts(
                "Proyecto 3", bigText)
            textRect.center = (int(1000/2), int(100))
            screen2.blit(text, textRect)
            text, textRect = self.texts(
                "Presiona A Para comenzar y ESC para salir.", smallText)
            textRect.center = (int(1000/2), int(250))
            screen2.blit(text, textRect)
            text, textRect = self.texts(
                "Salva a la niña y gana o topate con el fuego y pierde.", smallerText)
            textRect.center = (int(1000/2), int(400))
            screen2.blit(text, textRect)
            pygame.display.update()  
            clock.tick(15)  

    def lose(self):
        self.lose_music()
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        intro = False

            screen2.fill((0,0,0))
            smallText = pygame.font.Font('freesansbold.ttf', 40)
            bigText = pygame.font.Font('freesansbold.ttf', 90)

            text, textRect = self.texts("PERDISTE", bigText)
            textRect.center = (int(1000/2), int(100))
            screen2.blit(text, textRect)
            text, textRect = self.texts("Presiona ESC para salir.", smallText)
            textRect.center = (int(1000/2), int(250))
            screen2.blit(text, textRect)
            pygame.display.update()  
            clock.tick(15)

    def win(self):
        self.win_music()
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        intro = False

            screen2.fill((0,0,0))
            smallText = pygame.font.Font('freesansbold.ttf', 40)
            bigText = pygame.font.Font('freesansbold.ttf', 80)
            
            text, textRect = self.texts("MY MAN !!!! GANASTE", bigText)
            textRect.center = (int(1000/2), int(125))
            screen2.blit(text, textRect)
            text, textRect = self.texts("Presiona ESC para salir.", smallText)
            textRect.center = (int(1000/2), int(250))
            screen2.blit(text, textRect)
            pygame.display.update()  
            clock.tick(15)
    
    def mi_music(self):
        pygame.mixer.music.load('./mi.mp3')
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(0)

    def lose_music(self):
        pygame.mixer.music.load('./lose.mp3')
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(0)
    
    def win_music(self):
        pygame.mixer.music.load('./myman.mp3')
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(0)

pygame.init()
screen = pygame.display.set_mode((1000,500), pygame.DOUBLEBUF|pygame.HWACCEL)
r = Raycaster(screen)
r.load_map('./level1.txt')
screen2 = pygame.display.set_mode((1000,500))
pygame.display.set_caption('Lab 4')
clock = pygame.time.Clock()
r.menu()

# render loop
while True:

    screen.fill((0, 0, 0))
    r.render()
    d = 10
    start_time = pygame.time.get_ticks()
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            exit(0)
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                r.player["a"] -= pi/20
            if e.key == pygame.K_RIGHT:
                r.player["a"] += pi/20

            if e.key == pygame.K_UP:
                r.player["x"] += d * cos(r.player["a"])
                r.player["y"] += d * sin(r.player["a"])
            if e.key == pygame.K_DOWN:
                r.player["y"] -= d * cos(r.player["a"])
                r.player["y"] -= d * sin(r.player["a"])
            
            if (r.player["x"] > 300 and r.player["x"] < 345) and ( r.player["y"] > 400 and r.player["y"] < 445 ):
                r.win()

            if (r.player["x"] > 90 and r.player["x"] < 125) and ( r.player["y"] > 180 and r.player["y"] < 225 ):
                r.lose()
            
            if (r.player["x"] > 350 and r.player["x"] < 445) and ( r.player["y"] > 65 and r.player["y"] < 100 ):
                r.lose()
                #r.lose()
    screen.blit(r.getFps(), (900, 25))
    pygame.display.flip()

{
        "x":430,
        "y":75,
        "texture": pygame.image.load('./fire.jpg')
    }