from main import App
from Engine.scene import Scene

from OpenGL.GL import *
from pyrr import matrix44
import numpy


class RenderPass:

    def __init__(self, app: App):
        self.app = app

        self.projection_matrix = matrix44.create_perspective_projection(45, self.app.ASPECT, 0.1, 200, numpy.float32)
    
    def render(self, scene: Scene):
        self.view_matrix = matrix44.create_look_at(
            scene.camera.position,
            scene.camera.position + scene.camera.forward,
            scene.camera.up,
            numpy.float32
        )
        [m.setup() for m in self.app.graphics_engine.materials.values()]

        scene.render()
