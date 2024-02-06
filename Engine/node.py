from Engine.transform import Transform
from Engine.scene import Scene


class Node:

    def __init__(self, scene: Scene, name):
        self.scene = scene
        self.name = name

        self.transform = Transform(self)
        self.components = {}

        self.parent = None
        self.children = []

    def attempt_remove_self_from_parent(self):
        if self.parent:
            if self in self.parent.children:
                self.parent.children.remove(self)

    def set_parent(self, target):
        self.attempt_remove_self_from_parent()

        self.parent = target
        target.children.insert(0, self)
    
    def add_component(self, component, name=None):
        if not name:
            name = component.__class__.__name__

        if name in self.components:
            raise ValueError('Component name already exists')

        self.components[name] = component

    def physics_update(self):
        [c.physics_update() for c in self.components.values()]
        [c.physics_update() for c in self.children]

    def update(self):
        [c.update() for c in self.components.values()]
        [c.update() for c in self.children]

    def render(self):
        [c.render() for c in self.components.values()]
        [c.render() for c in self.children]
