#Gráficas por computadora
#Pablo Lopez 14509
#P1

from sr import *

glInit()
glCreateWindow(1000, 1000)
glViewPort(0, 0, 1000, 1000)
glClearColor(200, 200, 255)
glClear()

glLoad("bg.obj", "fondo.bmp", -1, 0, -500,  -90, "z", 516, 1153, 60, 1)
glDraw()
glLoad("warrior.obj", "gold.bmp", -34, 0, 0,  0, "y", 100, 100, 100, 5)
glDraw()
glLoad("bench.obj", "fondo.bmp", -602, -550, -200,  70, "y", 60, 60, 60, 4)
glDraw()
glLoad("penguin.obj", "gold.bmp", -200, -500, 0, 0, "x",400, 400, 400, 1)
glDraw()
glLoad("penguin.obj", "gold.bmp", 200, -500, 100, 0, "x", 400, 400, 400, 1)
glDraw()
glLoad("gun.obj", "fondo.bmp", -300, -280, 190, 75, "y", 9, 9, 9, 2)
glDraw()
glLoad("sword.obj", "gold.bmp", 370, -210, 150, 15, "y", 15, 20, 20, 3)
glDraw()
glFinish()

