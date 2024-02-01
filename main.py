import os
import sys
import pygame

sys.path.append('..')
sys.path.append('..\\..')


class App:
    DIR = os.getcwd()
    RES = WIDTH, HEIGHT = 800, 600
    ASPECT = WIDTH / HEIGHT
    FPS = 30
    NAME = ''

    def __init__(self):
        from Engine.graphics_engine.graphics_engine import GraphicsEngine
        
        self.graphics_engine = GraphicsEngine(self)
        self.active_scene = None

        self.clock = pygame.time.Clock()
        self.delta_time = 0

        self.running = False
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def run(self):
        self.running = True

        while self.running:
            self.delta_time = self.clock.tick(self.FPS)
            self.delta_time /= 1000

            self.check_events()
            self.active_scene.physics_update()
            self.active_scene.update()
            self.graphics_engine.render()

    def exit(self):
        self.graphics_engine.destroy()
        quit()
