from Engine.components.ui.image import Image
import pygame

class ScreenSurf(Image):

    def __init__(self, surface: pygame.Surface):
        super().__init__((0, 0), surface, None)
    
    def initialize(self):
        self.size = self.node.scene.app.RES
        self.rect = pygame.Rect(self.pos, self.size)
