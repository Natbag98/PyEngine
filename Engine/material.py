from OpenGL.GL import *
import re

from Engine.node import Node


class Material:

    def __init__(self):
        self.graphics_engine = None
        self.program = None

    def initialize(self):
        self.program = self.graphics_engine.compile_program('_'.join(re.split('(?<=.)(?=[A-Z])', self.__class__.__name__)).lower())
        glUseProgram(self.program)

        self.model_uniform_location = glGetUniformLocation(self.program, 'model')
        self.view_uniform_location = glGetUniformLocation(self.program, 'view')
        glUniformMatrix4fv(
            glGetUniformLocation(self.program, 'projection'),
            1,
            GL_FALSE,
            self.graphics_engine.render_pass.projection_matrix
        )
    
    def setup(self):
        glUseProgram(self.program)
        glUniformMatrix4fv(self.view_uniform_location, 1, GL_FALSE, self.graphics_engine.render_pass.view_matrix)

    def use(self, node: Node):
        glUseProgram(self.program)
        glUniformMatrix4fv(self.model_uniform_location, 1, GL_FALSE, node.transform.get_world_space_matrix())

    def destroy(self):
        glDeleteProgram(self.program)
