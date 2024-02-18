import numpy


class PointLight:

    def __init__(self, position, color, strength):
        self.scene = None

        self.position =  numpy.array(position, numpy.float32)
        self.color = color
        self.strength = strength
    
    def initialize(self):
        self.color = self.scene.app.graphics_engine.color_palatte[self.color]
