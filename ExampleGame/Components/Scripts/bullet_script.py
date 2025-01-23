from Engine.component import Component


class BulletScript(Component):

    def __init__(self, move_speed, move_dir):
        super().__init__()

        self.move_speed = move_speed
        self.move_dir = move_dir

    def update(self, app):
        self.node.transform.set_local_position(
            (
                self.node.transform.local_position[0],
                self.node.transform.local_position[1],
                self.node.transform.local_position[2] + self.move_dir * app.delta_time * self.move_speed
            )
        )

        if self.node.transform.local_position[2] > app.globals['MAX_Z'] + 40 or self.node.transform.local_position[2] < -1:
            self.node.destroy()
