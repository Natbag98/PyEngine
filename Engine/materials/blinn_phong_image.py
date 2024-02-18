from OpenGL.GL import *

from Engine.material import Material
from Engine.texture import Texture


class BlinnPhongImage(Material):

    def __init__(self, texture_path):
        super().__init__()

        self.texture_path = texture_path
    
    def initialize(self):
        super().initialize()

        self.texture = Texture(self.texture_path)

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

        self.texture.use()
