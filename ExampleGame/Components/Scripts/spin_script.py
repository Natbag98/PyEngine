from Engine.component import Component
from Engine.node import Node


class SpinScript(Component):

    def __init__(self, spin_speed):
        super().__init__()
        
        self.spin_speed = spin_speed

    def update(self):
        self.node.transform.set_eulers((0, 0, self.node.transform.eulers[2] + self.spin_speed * self.node.scene.app.delta_time))
