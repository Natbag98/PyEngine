from OpenGL.GL import *

from Engine.material import Material
from Engine.texture import Texture


class BlinnPhongSolid(Material):

    def __init__(self, color):
        super().__init__()

        self.color = color
    
    def initialize(self):
        super().initialize()

        self.color_uniform_location = glGetUniformLocation(self.program, 'color')

        self.point_light_location = {
            'position': glGetUniformLocation(self.program, 'point_light.position'),
            'color': glGetUniformLocation(self.program, 'point_light.color'),
            'strength': glGetUniformLocation(self.program, 'point_light.strength')
        }

    def use(self, node):
        super().use(node)

        light = self.graphics_engine.lights[0]
        glUniform3fv(self.point_light_location['position'], 1, light.position)
        glUniform3fv(self.point_light_location['color'], 1, light.color)
        glUniform1f(self.point_light_location['strength'], light.strength)

        glUniform3fv(self.color_uniform_location, 1, self.graphics_engine.color_palatte[self.color])
