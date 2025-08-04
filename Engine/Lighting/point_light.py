import numpy


class PointLight:

    def __init__(self, local_position, color, strength):
        self.scene = None

        self.local_position =  numpy.array(local_position, numpy.float32)
        self.color = color
        self.strength = strength

        self.parent = None

    def get_position(self):
        from Engine.scene import Scene
        if type(self.parent) == Scene:
            return self.local_position
        return self.parent.transform.get_global_position() + self.local_position

    def set_parent(self, target):
        from Engine.scene import Scene
        if type(target) == Scene:
            if not self.scene == target:
                raise ValueError('Cannot parent object outside of scene')
        else:
            if not self.scene == target.scene:
                raise ValueError('Cannot parent object outside of scene')

        self.parent = target
    
    def initialize(self):
        self.color = self.scene.app.graphics_engine.get_color(self.color)

    def destroy(self):
        self.scene.lights.remove(self)
