import pygame
from typing import Callable
from Engine.app import App
from Engine.component import Component

class Box(Component):

    def __init__(
        self,
        rect: pygame.Rect,
        color: str | tuple[int, int, int, int],
        border_weight: int=0,
        border_color: str | tuple[int,  int, int, int]=None
    ):
        super().__init__()

        self.rect = rect
        self.color = color
        self.border_weight = border_weight
        self.border_color = border_color

    def initialize(self):
        self.color = self.node.scene.app.graphics_engine.get_color(self.color)
        if self.border_color:
            self.border_color = self.node.scene.app.graphics_engine.get_color(self.border_color)

    def render_ui(self, surface):
        temp_surf = pygame.Surface(self.rect.size).convert_alpha()
        temp_surf.fill(self.node.scene.app.graphics_engine.get_pygame_color(self.color))
        if self.border_weight:
            pygame.draw.rect(
                temp_surf,
                self.node.scene.app.graphics_engine.get_pygame_color(self.border_color),
                (0, 0, self.rect.width, self.rect.height),
                self.border_weight,
            )
        surface.blit(temp_surf, self.rect.topleft)
