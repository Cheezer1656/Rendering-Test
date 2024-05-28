import numpy as np
from numba import njit


class Triangle:
    def __init__(self, v0, v1, v2, color=[255, 0, 0]):
        self.vertices = np.array([v0, v1, v2], dtype=np.float32)
        self.vertices = self.vertices[np.lexsort((self.vertices[:, 1], self.vertices[:, 0]))]
        self.color = np.array(color, dtype=np.uint32)

class Grid:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
        self.triangles = []
    
    def add_triangle(self, triangle):
        self.triangles.append(triangle)
    
    def render(self):
        result = np.zeros((self.height, self.width, self.depth, 3), dtype=np.uint32)
        for triangle in self.triangles:
            draw_triangle(result, triangle)
        return rasterize(result)

def rasterize(grid):
    result = np.zeros((grid.shape[0], grid.shape[1], 3), dtype=np.uint32)
    for i in np.flip(np.argwhere(grid.any(axis=3)), axis=0):
        color = grid[i[0], i[1], i[2]]
        color[0] = max(0, color[0] - i[2]*50)
        result[i[0], i[1]] = color
    return result

def connect_points(p1, p2):
    if p1[0] == p2[0]:
        result = np.empty((abs(p2[1] - p1[1]) + 1, 2), dtype=np.int32)
        for i, y in enumerate(range(min(p1[1], p2[1]), max(p1[1], p2[1]) + 1)):
            result[i] = [p1[0], y]
        return result
    if p1[0] > p2[0]:
        p1, p2 = p2, p1
    m = (p2[1] - p1[1]) / (p2[0] - p1[0])
    b = p1[1] - m * p1[0]

    result = np.empty((abs(p2[0] - p1[0] + 1), 2), dtype=np.int32)

    i = 0
    for x in range(p1[0], p2[0] + 1):
        y = round(m * x + b)
        result[i] = (x, y)
        i += 1

    return result

def draw_triangle(grid, triangle):
    v0, v1, v2 = triangle.vertices.round().astype(np.int32)
    l1a = connect_points(v0[:2], v1[:2])
    l1b = connect_points(v0[1:], v1[1:])
    l2a = connect_points(v1[:2], v2[:2])
    l2b = connect_points(v1[1:], v2[1:])
    l3a = connect_points(v2[:2], v0[:2])
    l3b = connect_points(v2[0::2], v0[0::2])

    for i in range(l1a.shape[0]):
        grid[l1a[i][0], l1a[i][1], l1b[l1a[i][1]-l1a[0][1]-1][1]] = triangle.color
    for i in range(l2a.shape[0]):
        grid[l2a[i][0], l2a[i][1], l2b[i][1]] = triangle.color
    for i in range(l3a.shape[0]):
        grid[l3a[i][0], l3a[i][1], l3b[i][1]] = triangle.color

def is_inside(v0, v1, v2, p):
    v0 = v0 - p
    v1 = v1 - p
    v2 = v2 - p
    c0 = np.cross(v0, v1)
    c1 = np.cross(v1, v2)
    c2 = np.cross(v2, v0)
    return np.dot(c0, c1) >= 0 and np.dot(c1, c2) >= 0 and np.dot(c2, c0) >= 0