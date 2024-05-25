import time

from matplotlib import pyplot as plt

from math_util import *
from util import *

width = 2000
height = 2000
img = Image(width, height)

tri1 = Triangle((10, 10), (20, 10), (15, 20))
tri1.scale(width / 100)
tri1.translate(0, 0)
img.add(tri1)

tri2 = Triangle((10, 10), (20, 10), (15, 20))
tri2.scale(width / 100)
tri2.translate(width, height)
img.add(tri2)

loops = 90
speed = width / loops

total_time = 0
display = Display(img.get())
for i in range(loops):
    start = time.time()
    tri1.rotate(1)
    tri1.scale(1.01)
    tri1.translate(speed, speed)
    tri2.rotate(-1)
    tri2.translate(-speed, -speed)
    tri2.scale(1.01)
    display.update(img.get())
    total_time += time.time() - start
    plt.pause(0.01)

print("Average time/frame:", total_time/360)