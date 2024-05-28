import matplotlib.pyplot as plt


class Display:
    def __init__(self, data):
        self.image = plt.imshow(data, interpolation='nearest')

    def update(self, data):
        self.image.set_data(data)
        plt.draw()