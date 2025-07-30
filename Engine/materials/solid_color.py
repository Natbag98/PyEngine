from OpenGL.GL import *

from Engine.material import Material


class SolidColor(Material):

    def __init__(self, color):
        super().__init__()

        self.color = color
    
    def initialize(self):
        super().initialize()

        self.color_uniform_location = glGetUniformLocation(self.program, 'color')
    
    def use(self, node):
        super().use(node)

        glUniform3fv(self.color_uniform_location, 1, self.graphics_engine.get_color(self.color))
