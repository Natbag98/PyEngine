from __future__ import annotations
from typing_extensions import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from node import Node

class Component:
    
    def __init__(self):
        self.node: "Node" = None

    def initialize(self):
        pass
    
    def physics_update(self):
        pass

    def update(self, app):
        pass

    def render(self):
        pass

    def render_ui(self, surface):
        pass

    def on_collider_hit(self, node):
        pass

    def ui_button_pressed(self, element):
        pass

    def destroy(self):
        pass
