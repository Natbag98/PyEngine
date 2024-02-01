from main import App
from scene import Scene

from OpenGL.GL import *
from pyrr import matrix44
import numpy


class RenderPass:

    def __init__(self, app: App, shader):
        self.app = app
        self.shader = shader
        glUseProgram(self.shader)

        projection_matrix = matrix44.create_perspective_projection(45, self.app.ASPECT, 0.1, 200, numpy.float32)
        glUniform4fv(
            glGetUniformLocation(self.shader, 'projection'),
            1,
            GL_FALSE,
            projection_matrix
        )
        self.model_uniform_location = glGetUniformLocation(self.shader, 'model')
        self.view_uniform_location = glGetUniformLocation(self.shader, 'view')

        self.color_uniform_location = glGetUniformLocation(self.shader, 'color')
    
    def render(self, scene: Scene):
        glUseProgram(self.shader)

        view_matrix = matrix44.create_look_at(
            scene.camera.position,
            scene.camera.position + scene.camera.forward,
            scene.camera.up,
            numpy.float32
        )
        glUniform4fv(self.view_uniform_location, 1, GL_FALSE, view_matrix)

        scene.render()
