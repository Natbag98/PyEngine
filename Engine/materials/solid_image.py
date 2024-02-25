from OpenGL.GL import *

from Engine.material import Material
from Engine.texture import Texture


class SolidImage(Material):

    def __init__(self, texture_path):
        super().__init__()

        self.texture_path = texture_path
    
    def initialize(self):
        super().initialize()

        self.texture = Texture(self.texture_path)
    
    def use(self, node):
        super().use(node)

        self.texture.use()
