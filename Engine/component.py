

class Component:
    
    def __init__(self):
        self.node = None

    def initialize(self):
        pass
    
    def physics_update(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

    def on_collider_hit(self, node):
        pass

    def destroy(self):
        pass
