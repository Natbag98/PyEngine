from Engine.component import Component
from Engine.node import Node
from Engine.components.render_mesh import RenderMesh

from  .enemy_script import EnemyScript

import random

from OpenGL.GL import GL_TRIANGLES


class GameManager(Component):

    def __init__(self, MIN_X, MAX_X, MAX_Z):
        self.min_spawn_time = 2
        self.max_spawn_time = 4
        self.time_till_next_spawn = 0

        self.MIN_X = MIN_X
        self.MAX_X = MAX_X
        self.MAX_Z = MAX_Z

    def update(self, app):
        self.time_till_next_spawn -= app.delta_time

        if self.time_till_next_spawn <= 0:
            self.time_till_next_spawn = random.randint(self.min_spawn_time, self.max_spawn_time)
            enemy = Node(app.active_scene, 'enemy')
            enemy.transform.set_local_position(
                (
                    random.randint(self.MIN_X, self.MAX_X),
                    0,
                    self.MAX_Z
                )
            )
            enemy.transform.set_scale((0.2, 0.2, 0.2))
            enemy.add_component(RenderMesh('ship', GL_TRIANGLES, 'teal'))
            enemy.add_component(EnemyScript(app.globals['ENEMY_MOVE_SPEED']))
            enemy.set_parent(app.active_scene)
