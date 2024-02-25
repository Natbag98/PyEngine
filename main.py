import os
import sys
import pygame

sys.path.append('..')
sys.path.append('..\\..')

from Engine.Utilities.window_properties import WindowProperties

from OpenGL.GL import *


class App:
    DIR = os.getcwd()
    SUPPORTED_OPENGL_GLSL_VERSIONS = {
        '3.2': '150',
        '3.3': '330',
        '4.0': '400',
        '4.1': '410',
        '4.2': '420',
        '4.3': '430',
        '4.4': '440',
        '4.5': '450',
        '4.6': '460'
    }

    def __init__(self, window_properties: WindowProperties=WindowProperties()):
        from Engine.graphics_engine.graphics_engine import GraphicsEngine

        self.RES = self.WIDTH, self.HEIGHT = window_properties.width, window_properties.height
        self.ASPECT = window_properties.width / window_properties.height
        self.FPS = window_properties.fps
        self.NAME = window_properties.name
        
        self.graphics_engine = GraphicsEngine(self)
        self.active_scene = None

        self.clock = pygame.time.Clock()
        self.delta_time = 0

        self.running = False

        self.GL_VERSION = glGetString(GL_VERSION).decode('utf-8').split(' ')[0]
        if self.GL_VERSION[:3] not in self.SUPPORTED_OPENGL_GLSL_VERSIONS:
            raise Exception(
                f'OpenGL version {self.GL_VERSION} not supported in this project.',
            )

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def run(self):
        self.running = True

        while self.running:
            self.delta_time = self.clock.tick(self.FPS)
            self.delta_time /= 1000

            frame_rate = 1 / self.delta_time
            pygame.display.set_caption(str(frame_rate))

            self.check_events()
            self.active_scene.physics_update()
            self.active_scene.update()
            self.graphics_engine.render(self.active_scene)

    def exit(self):
        self.graphics_engine.destroy()
        quit()
