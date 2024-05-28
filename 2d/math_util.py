from math import cos, radians, sin

import numpy as np
from numba import njit


class Triangle:
    def __init__(self, p1, p2, p3):
        self.points = np.array([p1, p2, p3], dtype=np.float64)
    def __getitem__(self, index):
        return np.round(self.points[index]).astype(np.int32)
    def translate(self, x, y):
        self.points += (x, y)
    def rotate(self, degrees):
        centerX = np.average(self.points[:, 0])
        centerY = np.average(self.points[:, 1])
        self.points -= (centerX, centerY)
        for p in self.points:
            p[0], p[1] = rotate_point(p, degrees)
        self.points += (centerX, centerY)
    def scale(self, factor):
        centerX = np.average(self.points[:, 0])
        centerY = np.average(self.points[:, 1])
        self.points -= (centerX, centerY)
        self.points *= factor
        self.points += (centerX, centerY)

class Image:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.triangles = []
    
    def add(self, triangle):
        self.triangles.append(triangle)

    def draw_triangle(self, triangle):
        draw_triangle(self.pixels, triangle[0], triangle[1], triangle[2])
    
    def get(self):
        self.pixels = np.zeros((self.height, self.width))
        for triangle in self.triangles:
            self.draw_triangle(triangle)
        return self.pixels

@njit(cache=True)
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

@njit(cache=True)
def rotate_point(p, degrees):
    degrees = radians(degrees)
    x = p[0] * cos(degrees) - p[1] * sin(degrees)
    y = p[0] * sin(degrees) + p[1] * cos(degrees)
    return x, y

@njit(cache=True)
def draw_triangle(pixels, p1, p2, p3):
    l1 = connect_points(p1, p2)
    l2 = connect_points(p2, p3)
    l3 = connect_points(p3, p1)
    
    line_points = np.concatenate((l1, l2, l3))
    points = np.concatenate((p1, p2, p3)).reshape(3, 2)
    for x in range(np.min(points[:, 0]), np.max(points[:, 0]) + 1):
        if x >= 0 and x < pixels.shape[1]:
            ys = np.sort(line_points[line_points[:, 0] == x][:, 1])
            for i in range(ys[0], ys[-1] + 1):
                if i >= 0 and i < pixels.shape[0]:
                    pixels[i, x] = 1