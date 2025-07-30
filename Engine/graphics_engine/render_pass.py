from Engine.app import App
from Engine.scene import Scene
from Engine.texture import Texture
from Engine.mesh import Mesh

from OpenGL.GL import *
from pyrr import matrix44, Vector3
import numpy
import pygame


class RenderPass:

    def __init__(self, app: App):
        self.app = app

        self.projection_matrix = matrix44.create_perspective_projection(45, self.app.ASPECT, 0.1, 200, numpy.float32)
        self.orthographic_projection_matrix_2d = matrix44.create_orthogonal_projection_matrix(0, app.WIDTH, app.HEIGHT, 0, -1, 1)

        self.ui_program = None
        self.ui_projection_location = None
        self.ui_model_location = None
        self.ui_image_location = None
    
    def render(self, scene: Scene):
        # Render meshes
        self.view_matrix = matrix44.create_look_at(
            scene.camera.position,
            scene.camera.position + scene.camera.forward,
            scene.camera.up,
            numpy.float32
        )
        [m.setup() for m in self.app.graphics_engine.materials.values()]
        scene.render()

        # Update ui program
        if not self.ui_program:
            self.ui_program = self.app.graphics_engine.compile_program('ui')
            self.ui_projection_location = glGetUniformLocation(self.ui_program, 'projection')
            self.ui_model_location = glGetUniformLocation(self.ui_program, 'model')
            self.ui_image_location = glGetUniformLocation(self.ui_program, 'imageTexture')

        # Render ui to pygame surface
        ui_surface = pygame.Surface(self.app.RES).convert_alpha()
        ui_surface.fill((0, 0, 0, 0))
        scene.render_ui(ui_surface)

        # test draw
        # rect = pygame.Rect(100, 100, 200, 200)
        # temp_surf = pygame.Surface(rect.size).convert_alpha()
        # temp_surf.fill((255, 255, 255, 128))
        # ui_surface.blit(temp_surf, rect.topleft)

        # Setup ui shader
        glUseProgram(self.ui_program)
        glUniformMatrix4fv(self.ui_projection_location, 1, GL_FALSE, self.orthographic_projection_matrix_2d)
        glUniformMatrix4fv(self.ui_model_location, 1, GL_FALSE, matrix44.create_from_scale(Vector3([self.app.WIDTH, self.app.HEIGHT, 1.0])))

        # Setup ui texture
        ui_texture = Texture(None, ui_surface)
        ui_texture.use()

        # Draw ui surface to screen
        glBindVertexArray(self.app.graphics_engine.meshes['ui_quad'].vertex_array_object)
        glDrawArrays(GL_TRIANGLES, 0, self.app.graphics_engine.meshes['ui_quad'].vertex_count)
        glBindVertexArray(0)

        # Cleanup ui texture
        ui_texture.destroy()
