from main import App
from Engine.graphics_engine.render_pass import RenderPass
from Engine.mesh import Mesh
from Engine.material import Material

import pygame
import numpy
from OpenGL.GL.shaders import compileShader, compileProgram
from OpenGL.GL import *

class GraphicsEngine:

    def __init__(self, app: App):
        self.app = app

        self.meshes = {}
        self.materials = {}
        self.lights = []

        colors = {
            'navy': (0, 13, 107),
            'red': (255, 0, 0),
            'black': (0, 0, 0)
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
        glClearColor(self.color_palatte['black'][0], self.color_palatte['black'][1], self.color_palatte['black'][2], 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.render_pass = RenderPass(self.app)

        # Display OpenGL version
        gl_vendor = glGetString(GL_VENDOR).decode('utf-8')
        gl_version = glGetString(GL_VERSION).decode('utf-8')
        gl_renderer = glGetString(GL_RENDERER).decode('utf-8')
        glsl_version = glGetString(GL_SHADING_LANGUAGE_VERSION).decode('utf-8')

        print('OpenGL info:')
        print(f'GL Vendor    : {gl_vendor}')
        print(f'GL Renderer  : {gl_renderer}')
        print(f'GL Version   : {gl_version}')
        print(f'GLSL Version : {glsl_version}')

    def new_material(self, material: Material, name):
        if name in self.materials:
            raise ValueError(f'{name} is already the name of a material')
        
        material.graphics_engine = self
        material.initialize()
        self.materials[name] = material
    
    def new_mesh(self, file_name, name):
        if name in self.meshes:
            raise ValueError(f'{name} is already the name of a mesh')

        self.meshes[name] = Mesh(file_name)
    
    def compile_shader_src(self, src: list[str]):
        supported_version = self.app.SUPPORTED_OPENGL_GLSL_VERSIONS[self.app.GL_VERSION[:3]]
        shader_version = src[0].split(' ')[1]
        if not shader_version == supported_version:
            src[0] = src[0].replace(shader_version, supported_version)
        return src

    def compile_program(self, material_name):
        with open(f'{self.app.DIR}\\Engine\\shaders\\{material_name}\\vertex.glsl', 'r') as file:
            vertex_src = self.compile_shader_src(file.readlines())

        with open(f'{self.app.DIR}\\Engine\\shaders\\{material_name}\\fragment.glsl', 'r') as file:
            fragment_src = self.compile_shader_src(file.readlines())
        
        program = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        return program

    def render(self, scene):
        self.lights = self.app.active_scene.lights

        glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)
        self.render_pass.render(scene)
        pygame.display.flip()

    def destroy(self):
        [m.destroy() for m in self.meshes]
        [m.destroy() for m in self.materials]
        pygame.quit()
