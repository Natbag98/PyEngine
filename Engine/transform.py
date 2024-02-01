import numpy


class Transform:

    def __init__(self, node):
        self.node = node

        self.local_position = numpy.array([0, 0, 0], numpy.float32)
        self.global_position = numpy.array([0, 0, 0], numpy.float32)
        self.rotation = numpy.array([0, 0, 0], numpy.float32)
        self.scale = numpy.array([1, 1, 1], numpy.float32)
