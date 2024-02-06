from Engine.node import Node


class Component:
    
    def __init__(self, node: Node):
        self.node = node
    
    def physics_update(self):
        pass

    def update(self):
        pass

    def render(self):
        pass
