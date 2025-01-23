from Engine.scene import Scene
from Engine.component import Component


class Node:

    def __init__(self, scene: Scene, name):
        self.scene = scene

        if name == 'Scene':
            raise ValueError('Cannot name node \'Scene\'')
        self.name = name

        from Engine.transform import Transform

        self.transform = Transform(self)
        self.components = {}

        self.tag = ''

        self.parent = None
        self.children = []
        self.lights = []

    def attempt_remove_self_from_parent(self):
        if self.parent:
            if self in self.parent.children:
                self.parent.children.remove(self)

    def set_parent(self, target):
        self.attempt_remove_self_from_parent()

        if target.name == 'Scene':
            if not self.scene == target:
                raise ValueError('Cannot parent object outside of scene')
        else:
            if not self.scene == target.scene:
                raise ValueError('Cannot parent object outside of scene')

        self.parent = target
        target.children.append(self)
    
    def has_component(self, component: Component):
        return component.__name__ in self.components.keys()
    
    def get_component(self, component: Component):
        return self.components[component.__name__]
    
    def add_component(self, component: Component):
        name = component.__class__.__name__

        if name in self.components:
            raise ValueError('Component name already exists')

        component.node = self
        component.initialize()
        self.components[name] = component
    
    def get_nodes_with_tag(self, tag):
        nodes_with_tag = []
        if self.tag == tag:
            nodes_with_tag.append(self)
        for c in self.children:
            for node in c.get_nodes_with_tag(tag):
                nodes_with_tag.append(node)
        return nodes_with_tag

    def physics_update(self):
        [c.physics_update() for c in self.components.values()]
        [c.physics_update() for c in self.children]

    def update(self, app):
        [c.update(app) for c in self.components.values()]
        [c.update(app) for c in self.children]

    def render(self):
        [c.render() for c in self.components.values()]
        [c.render() for c in self.children]
    
    def destroy(self):
        [c.destroy() for c in self.components.values()]
        [c.destroy() for c in self.children]

        self.attempt_remove_self_from_parent()
        for light in self.lights:
            light.destroy()
