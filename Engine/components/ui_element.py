import pygame
from Engine.component import Component

from OpenGL.GL import *

class UIElement(Component):

    def __init__(
        self,
        pos,
        text=None,
        text_size=None,
        font=None,
        text_color='black',
        color='white',
        size=None
    ):
        self.rect = None
        self.size = size
        self.pos = pos
        self.text = text
        self.text_size = text_size
        self.font = font
        self.text_color = text_color
        self.color = color

    def initialize(self):
        if self.text:
            self.render_text()

        self.rect = pygame.Rect(self.pos, self.size)

    def render_text(self):
        sys_font = pygame.font.SysFont(self.font, self.text_size)
        if type(self.text) not in [str, bytes]:
            self.text = ' '
        self.text = sys_font.render(self.text, True, self.text_color)
        self.size = self.text.get_size()

    def update(self, app):
        if app.input.mouse['left'].interact(self.rect, 'clicked'):
            [c.ui_button_pressed(self) for c in self.node.components.values()]

    def render_ui(self, surface):
        surface.blit(self.text, self.rect)
