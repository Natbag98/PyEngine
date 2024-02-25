from OpenGL.GL import *

from Engine.material import Material
from Engine.texture import Texture


class BlinnPhongSolid(Material):

    def __init__(self, color, ambient_lighting=None, specular_strength=None):
        super().__init__()

        self.color = color
        self.ambient_lighting = ambient_lighting
        self.specular_strength = specular_strength
    
    def initialize(self):
        super().initialize()

        self.color_uniform_location = glGetUniformLocation(self.program, 'color')
        self.ambient_light_location = glGetUniformLocation(self.program, 'ambient_light')
        self.specular_strength_location = glGetUniformLocation(self.program, 'specular_strength')
        self.camera_position_location = glGetUniformLocation(self.program, 'camera_position')

        self.point_lights_location = {
            'position': [
                glGetUniformLocation(self.program, f'point_lights[{i}].position')
                for i in range(self.graphics_engine.max_lights)
            ],
            'color': [
                glGetUniformLocation(self.program, f'point_lights[{i}].color')
                for i in range(self.graphics_engine.max_lights)
            ],
            'strength': [
                glGetUniformLocation(self.program, f'point_lights[{i}].strength')
                for i in range(self.graphics_engine.max_lights)
            ],
        }

    def use(self, node):
        super().use(node)

        if self.ambient_lighting:
            glUniform1f(self.ambient_light_location, self.ambient_lighting)
        else:
            glUniform1f(self.ambient_light_location, node.scene.ambient_lighting)
        
        if self.specular_strength:
            glUniform1f(self.specular_strength_location, self.specular_strength)
        else:
            glUniform1f(self.specular_strength_location, node.scene.specular_strength)
        
        glUniform3fv(self.camera_position_location, 1, node.scene.camera.position)

        for i, light in enumerate(self.graphics_engine.lights):
            glUniform3fv(self.point_lights_location['position'][i], 1, light.position)
            glUniform3fv(self.point_lights_location['color'][i], 1, light.color)
            glUniform1f(self.point_lights_location['strength'][i], light.strength)

        glUniform3fv(self.color_uniform_location, 1, self.graphics_engine.color_palatte[self.color])
