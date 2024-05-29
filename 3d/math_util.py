from colorsys import rgb_to_hsv, hsv_to_rgb

import numpy as np
from numba import njit


class Triangle:
    def __init__(self, v0, v1, v2, color=[255, 0, 0]):
        self.vertices = np.array([v0, v1, v2], dtype=np.int32)
        self.vertices = self.vertices[np.lexsort((self.vertices[:, 1], self.vertices[:, 0]))]
        self.color = np.array(color, dtype=np.uint32)

class Grid:
    def __init__(self, width, height, depth, light=[0, 0, 0], light_intensity=1.5):
        self.width = width
        self.height = height
        self.depth = depth
        self.light = np.array(light, dtype=np.int32)
        self.light_intensity = light_intensity
        self.triangles = []
    
    def add_triangle(self, triangle):
        self.triangles.append(triangle)
    
    def render(self):
        result = np.zeros((self.height, self.width, self.depth, 3), dtype=np.uint32)
        for triangle in self.triangles:
            draw_triangle(result, triangle)
        return rasterize(result, self.light, self.light_intensity)

def rasterize(grid, light, intensity):
    result = np.zeros((grid.shape[0], grid.shape[1], 3), dtype=np.uint32)
    radius = np.linalg.norm(np.array(grid.shape[:2]) / 2)
    points = np.flip(np.argwhere(grid.any(axis=3)), axis=0)
    for p in points:
        distance = np.linalg.norm(p - light) / intensity
        hsv = rgb_to_hsv(*(grid[p[0], p[1], p[2]])/255)
        result[p[0], p[1]] = (np.array(hsv_to_rgb(hsv[0], hsv[1], max(0, 1 - distance / radius)))*255)
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

    apoints = np.concatenate([l1a, l2a, l3a])
    bpoints = np.concatenate([l1b, l2b, l3b])
    for i in range(min(apoints[:, 0]), max(apoints[:, 0]) + 1):
        if i >= 0 and i < grid.shape[0]:
            ys = np.sort(apoints[apoints[:, 0] == i][:, 1])
            zs = np.sort(bpoints[bpoints[:, 0] == i][:, 1])
            l4a = connect_points([i, ys[0]], [i, ys[-1]])
            l4b = connect_points([ys[0], zs[0]], [ys[-1], zs[-1]])
            for j in range(l4a.shape[0]):
                grid[i, l4a[j][1], l4b[j][1]] = triangle.color

def is_inside(v0, v1, v2, p):
    v0 = v0 - p
    v1 = v1 - p
    v2 = v2 - p
    c0 = np.cross(v0, v1)
    c1 = np.cross(v1, v2)
    c2 = np.cross(v2, v0)
    return np.dot(c0, c1) >= 0 and np.dot(c1, c2) >= 0 and np.dot(c2, c0) >= 0