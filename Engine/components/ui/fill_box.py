from Engine.component import Component
import pygame

class FillBox(Component):

    def __init__(
        self,
        rect: pygame.Rect,
        color: str | tuple[int, int, int, int],
        fill_from: str,
        back_color: str | tuple[int, int, int, int],
        border_weight: int=0,
        border_color: str | tuple[int, int, int, int]=None
    ):
        super().__init__()

        self.rect = self.fill_rect = rect
        self.fill = 100
        self.color = color
        self.fill_from = fill_from
        self.back_color = back_color
        self.border_weight = border_weight
        self.border_color = border_color

    def initialize(self):
        self.color = self.node.scene.app.graphics_engine.get_color(self.color)
        self.back_color = self.node.scene.app.graphics_engine.get_color(self.back_color)
        if self.border_color:
            self.border_color = self.node.scene.app.graphics_engine.get_color(self.border_color)

    def update(self, app):
        top = self.rect.top
        left = self.rect.left
        width = self.rect.width
        height = self.rect.height

        if self.fill > 100:
            self.fill = 100

        if self.fill_from == 'bottom':
            height = self.rect.height * (self.fill / 100) + 1
            top += self.rect.height - self.rect.height * (self.fill / 100)
        elif self.fill_from == 'top':
            height = self.rect.height * (self.fill / 100)
        elif self.fill_from == 'left':
            width = self.rect.width * (self.fill / 100)
        elif self.fill_from == 'right':
            width = self.rect.width * (self.fill / 100) + 1
            left += self.rect.width - self.rect.width * (self.fill / 100)
        else:
            raise Exception(f'Invalid fill: {self.fill_from}')

        self.fill_rect = pygame.Rect(
            left - self.rect.left,
            top - self.rect.top,
            width,
            height
        )

    def render_ui(self, surface):
        temp_surf = pygame.Surface(self.rect.size).convert_alpha()
        temp_surf.fill(self.node.scene.app.graphics_engine.get_pygame_color(self.back_color))
        pygame.draw.rect(temp_surf, self.node.scene.app.graphics_engine.get_pygame_color(self.color), self.fill_rect)
        if self.border_weight:
            pygame.draw.rect(
                temp_surf,
                self.node.scene.app.graphics_engine.get_pygame_color(self.border_color),
                (0, 0, self.rect.width, self.rect.height),
                self.border_weight,
            )
        surface.blit(temp_surf, self.rect.topleft)
