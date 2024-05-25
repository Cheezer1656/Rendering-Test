import matplotlib.pyplot as plt
import numpy as np


class Display:
    def __init__(self, pixels):
        data = np.zeros((pixels.shape[0], pixels.shape[1], 3))
        data[pixels == 1] = [1, 1, 1]
        self.image = plt.imshow(data, interpolation='nearest')
        
    def update(self, pixels):
        data = np.zeros((pixels.shape[0], pixels.shape[1], 3))
        data[pixels == 1] = [1, 1, 1]
        self.image.set_data(data)
        plt.draw()