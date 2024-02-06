from Engine.component import Component
from Engine.mesh import Mesh

from OpenGL.GL import *


class RenderMesh(Component):
    
    def __init__(self, node, mesh_name, draw_mode, color):
        super().__init__(node)
        self.render_pass = self.node.scene.app.graphics_engine.render_pass

        self.mesh = self.node.scene.app.graphics_engine.meshes[mesh_name]
        self.draw_mode = draw_mode
        self.color = color
    
    def render(self):
        glUniformMatrix3fv(self.render_pass.color_uniform_location, 1, GL_FALSE, self.node.scene.app.graphics_engine.color_palatte[self.color])
        glUniformMatrix4fv(self.render_pass.model_uniform_location, 1, GL_FALSE, self.node.transform.get_world_space_matrix())
        glBindVertexArray(self.mesh.vertex_array_object)
        glDrawArrays(self.draw_mode, 0, self.mesh.vertex_count)
