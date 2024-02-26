from main import App
from Engine.camera import Camera
from Engine.Lighting.point_light import PointLight


class Scene:

    def __init__(self, app: App):
        self.app = app
        self.name = 'Scene'

        self.children = []
        self.camera = Camera()

        self.lights = []
        self.ambient_lighting = 0.2
        self.specular_strength = 32
    
    def new_light(self, light: PointLight):
        if len(self.lights) == self.app.graphics_engine.max_lights:
            raise Exception('Max lights reached')

        light.scene = self
        light.initialize()
        self.lights.append(light)
    
    def physics_update(self):
        [c.physics_update() for c in self.children]

    def update(self):
        [c.update() for c in self.children]

    def render(self):
        [c.render() for c in self.children]
    
    def destroy(self):
        [c.destroy() for c in self.children]
