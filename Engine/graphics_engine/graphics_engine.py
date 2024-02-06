from main import App
from Engine.graphics_engine.render_pass import RenderPass
from Engine.mesh import Mesh

import pygame
import numpy
from OpenGL.GL.shaders import compileShader, compileProgram
from OpenGL.GL import *

class GraphicsEngine:

    def __init__(self, app: App):
        self.app = app

        self.meshes = {}

        colors = {
            'navy': (0, 13, 107),
            'red': (255, 0, 0)
        }

        self.color_palatte = {
            color: numpy.array([colors[color][0] / 255, colors[color][1] / 255, colors[color][2] / 255], dtype=numpy.float32)
            for color in colors
        }

        # Init pygame
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.set_mode(self.app.RES, pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption(self.app.NAME)

        # Init OpenGL
        glClearColor(self.color_palatte['navy'][0], self.color_palatte['navy'][1], self.color_palatte['navy'][2], 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.shader = self.compile_shader('vertex.glsl', 'fragment.glsl')
        self.render_pass = RenderPass(self.app, self.shader)
    
    def new_mesh(self, file_name, name):
        if name in self.meshes:
            raise ValueError(f'{name} is already the name of a mesh')

        self.meshes[name] = Mesh(file_name)

    def compile_shader(self, vertex_file_name, fragment_file_name):
        with open(f'{self.app.DIR}\\Engine\\shaders\\{vertex_file_name}', 'r') as file:
            vertex_src = file.readlines()
        
        with open(f'{self.app.DIR}\\Engine\\shaders\\{fragment_file_name}', 'r') as file:
            fragment_src = file.readlines()
        
        return compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

    def render(self, scene):
        glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)
        self.render_pass.render(scene)
        pygame.display.flip()

    def destroy(self):
        [m.destroy() for m in self.meshes]
        self.render_pass.destroy()
        pygame.quit()
