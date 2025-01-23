from Engine.component import Component


class EnemyScript(Component):

    def __init__(self, move_speed):
        super().__init__()

        self.move_speed = move_speed

    def update(self, app):
        self.node.transform.set_local_position(
            (
                self.node.transform.local_position[0],
                self.node.transform.local_position[1],
                self.node.transform.local_position[2] + app.delta_time * -self.move_speed
            )
        )

        if self.node.transform.local_position[2] < -1:
            self.node.destroy()
