from main import App
from Engine.camera import Camera
from Engine.Lighting.point_light import PointLight


class Scene:

    def __init__(self, app: App):
        self.app = app
        self.name = 'Scene'

        self.children = []
        self.lights = []
        self.ambient_lighting = 0.2
        self.camera = Camera()
    
    def new_light(self, light: PointLight):
        light.scene = self
        light.initialize()
        self.lights.append(light)
    
    def physics_update(self):
        [c.physics_update() for c in self.children]

    def update(self):
        [c.update() for c in self.children]

    def render(self):
        [c.render() for c in self.children]
