import time

from math_util import *
from matplotlib import pyplot as plt
from util import *

start = time.time()

tri = Triangle([0, 0, 0], [0, 9, 4], [9, 0, 4])
# tri = Triangle([4, 1, 4], [8, 9, 0], [0, 7, 4])

grid = Grid(10, 10, 5)
grid.add_triangle(tri)
display = Display(grid.render())

print("Time to render:", time.time() - start)

plt.show()