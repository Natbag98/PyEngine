import pygame
from typing import Callable
from Engine.app import App
from Engine.component import Component

class Button(Component):

    def __init__(
        self,
        pos: tuple[int, int],
        color: str | tuple[int, int, int, int],
        size: tuple[int, int],
        input_key: str,
        click_type: str,
        clicked_func_tuple: tuple[Callable[[App, "Button"], None]]=()
    ):
        super().__init__()

        self.rect = pygame.Rect(pos, size)
        self.color = color
        self.input_key = input_key
        self.click_type = click_type
        self.clicked_func_tuple = clicked_func_tuple

    def initialize(self):
        self.color = self.node.scene.app.graphics_engine.get_color(self.color)

    def update(self, app):
        if app.input.mouse[self.input_key].interact(self.rect, self.click_type):
            for func in self.clicked_func_tuple:
                func(app, self)

    def render_ui(self, surface):
        temp_surf = pygame.Surface(self.rect.size).convert_alpha()
        temp_surf.fill((0, 0, 0, 0))
        pygame.draw.rect(
            temp_surf,
            self.node.scene.app.graphics_engine.get_pygame_color(self.color),
            (0, 0, self.rect.width, self.rect.height)
        )
        surface.blit(temp_surf, self.rect.topleft)
