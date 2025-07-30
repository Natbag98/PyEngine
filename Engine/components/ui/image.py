import pygame
from Engine.component import Component

class Image(Component):

    def __init__(
        self,
        pos: tuple[int, int],
        image: pygame.Surface | str,
        size: tuple[int, int]=None
    ):
        super().__init__()

        self.pos = pos
        self.image = image
        self.size = size
        self.rect = None

    def initialize(self):
        if type(self.image) == str:
            self.image = pygame.image.load(self.image).convert_alpha()

        if not self.size:
            self.size = self.image.get_size()
        else:
            self.image = pygame.transform.scale(self.image, self.size)

        self.rect = pygame.Rect(self.pos, self.size)

    def render_ui(self, surface):
        surface.blit(self.image, self.rect)
