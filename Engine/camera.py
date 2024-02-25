import numpy


class Camera:

    def __init__(self, position=(0, 0, 0), forward=(0, 0, 1), up=(0, 1, 0)):
        self.position = numpy.array(position, numpy.float32)
        self.forward = numpy.array(forward, numpy.float32)
        self.up = numpy.array(up, numpy.float32)
