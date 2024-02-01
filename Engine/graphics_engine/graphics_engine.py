import sys
sys.path.append('..\\..')

from main import App

import pygame
import numpy
from OpenGL.GL.shaders import compileShader, compileProgram
from OpenGL.GL import *

class GraphicsEngine:

    def __init__(self, app: App):
        self.app = app

        colors = {
            'Navy': (0, 13, 107)
        }

        self.color_palatte = {
            self.color_palatte[color]: numpy.array([colors[color][0] / 255, colors[color][1] / 255, colors[color][2] / 255], dtype=numpy.float32)
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
        glClearColor(self.color_palatte['Navy'][0], self.color_palatte['Navy'][1], self.color_palatte['Navy'][2], 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.shader = self.compile_shader('vertex.glsl', 'fragment.glsl')
        self.render_pass = None
    
    def compile_shader(self, vertex_file_name, fragment_file_name):
        with open(f'{self.app.DIR}\\Engine\\shaders\\{vertex_file_name}', 'r') as file:
            vertex_src = file.readlines()
        
        with open(f'{self.app.DIR}\\Engine\\shaders\\{fragment_file_name}', 'r') as file:
            fragment_src = file.readlines()
        
        return compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

    def render(self):
        pass

    def destroy(self):
        pygame.quit()
