import pygame
from Engine.component import Component

from OpenGL.GL import *

class TextElement(Component):

    def __init__(
        self,
        pos,
        text=None,
        text_size=None,
        font=None,
        text_color='black'
    ):
        super().__init__()

        self.rect = None
        self.pos = pos
        self.text = text
        self.text_size = text_size
        self.font = font
        self.text_color = text_color

    def initialize(self):
        self.text_color = self.node.scene.app.graphics_engine.get_color(self.text_color)
        self.render_text()

    def render_text(self):
        sys_font = pygame.font.SysFont(self.font, self.text_size)
        if type(self.text) not in [str, bytes]:
            self.text = ' '
        self.text = sys_font.render(self.text, True, self.node.scene.app.graphics_engine.get_pygame_color(self.text_color))
        self.size = self.text.get_size()
        self.rect = pygame.Rect(self.pos, self.size)

    def render_ui(self, surface):
        temp_surf = pygame.Surface(self.rect.size).convert_alpha()
        temp_surf.fill((0, 0, 0, 0))
        temp_surf.blit(self.text, (0, 0))
        surface.blit(temp_surf, self.rect.topleft)
