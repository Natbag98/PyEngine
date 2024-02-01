from main import App
from Engine.camera import Camera


class Scene:

    def __init__(self, app: App):
        self.app = app

        self.children = []
        self.camera = Camera()
    
    def physics_update(self):
        [c.physics_update() for c in self.children]

    def update(self):
        [c.update() for c in self.children]

    def render(self):
        [c.render() for c in self.children]
