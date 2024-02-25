from Engine.component import Component
from Engine.mesh import Mesh

from OpenGL.GL import *
import numpy


class RenderMesh(Component):
    
    def __init__(self, mesh_name, draw_mode, material_name):
        super().__init__()
        self.mesh_name = mesh_name
        self.draw_mode = draw_mode
        self.material_name = material_name
    
    def initialize(self):
        self.render_pass = self.node.scene.app.graphics_engine.render_pass
        self.mesh = self.node.scene.app.graphics_engine.meshes[self.mesh_name]
        self.material = self.node.scene.app.graphics_engine.materials[self.material_name]
    
    def render(self):
        self.material.use(self.node)
        glBindVertexArray(self.mesh.vertex_array_object)
        glDrawArrays(self.draw_mode, 0, self.mesh.vertex_count)
