import numpy
from pyrr import matrix44


class Transform:

    def __init__(self, node):
        self.node = node

        self.local_position = numpy.array([0, 0, 0], numpy.float32)
        self.global_position = numpy.array([0, 0, 0], numpy.float32)
        self.eulers = numpy.array([0, 0, 0], numpy.float32)
        self.scale = numpy.array([1, 1, 1], numpy.float32)
    
    def set_local_position(self, val: list | tuple):
        self.local_position = numpy.array(val, numpy.float32)
    
    def set_global_position(self, val: list | tuple):
        self.global_position = numpy.array(val, numpy.float32)
    
    def set_eulers(self, val: list | tuple):
        self.eulers = numpy.array(val, numpy.float32)
    
    def set_scale(self, val: list | tuple):
        self.scale = numpy.array(val, numpy.float32)
    
    def get_world_space_matrix(self):
        model_matrix = matrix44.create_identity(numpy.float32)
        model_matrix = matrix44.multiply(
            model_matrix,
            matrix44.create_from_eulers(numpy.radians(self.eulers), numpy.float32)
        )
        model_matrix = matrix44.multiply(
            model_matrix,
            matrix44.create_from_scale(self.scale, numpy.float32)
        )
        model_matrix = matrix44.multiply(
            model_matrix,
            matrix44.create_from_translation(self.global_position, numpy.float32)
        )
        return model_matrix
