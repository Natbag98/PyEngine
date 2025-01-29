from Engine.app import App
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
    
    def new_light(self, light: PointLight, parent):
        if len(self.lights) == self.app.graphics_engine.max_lights:
            raise Exception('Max lights reached')

        light.scene = self
        light.set_parent(parent)
        if not parent.name == 'Scene':
            parent.lights.append(light)
        light.initialize()
        self.lights.append(light)

    def get_all_nodes_with_tag(self, tag):
        nodes_with_tag = []
        for c in self.children:
            for node in c.get_nodes_with_tag(tag):
                nodes_with_tag.append(node)
        return nodes_with_tag

    def physics_update(self):
        [c.physics_update() for c in self.children]

    def update(self, app):
        [c.update(app) for c in self.children]

    def render(self):
        [c.render() for c in self.children]

    def render_ui(self):
        [c.render_ui() for c in self.children]
    
    def destroy(self):
        [c.destroy() for c in self.children]
