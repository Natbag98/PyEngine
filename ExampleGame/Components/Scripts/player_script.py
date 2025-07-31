from Engine.component import Component
from Engine.components.render_mesh import RenderMesh
from Engine.components.collider import Collider
from Engine.Lighting.point_light import PointLight
from Engine.node import Node
import pygame

from .bullet_script import BulletScript

from OpenGL.GL import GL_TRIANGLES

class PlayerScript(Component):
    reload_speed = 3
    bullet_light_pos = {
        'left': (0.5, 0, 0),
        'right': (-0.5, 0, 0),
    }

    def __init__(self, max_x, min_x, move_speed):
        super().__init__()

        self.max_x = max_x
        self.min_x = min_x
        self.move_speed = move_speed
        self.reload_timers = {'left': self.reload_speed, 'right': self.reload_speed}

    def shoot_bullet(self, app, side: str):
        if not self.reload_timers[side] > self.reload_speed:
            return
        self.reload_timers[side] = 0

        bullet = Node(self.node.scene, 'bullet')
        bullet.tag = 'bullet'
        bullet.set_parent(self.node.scene)

        bullet.transform.set_local_position(self.node.transform.local_position)
        bullet.transform.set_scale((0.2, 0.2, 0.2))
        bullet.transform.set_eulers((90, 90, 0))

        bullet.add_component(RenderMesh(f'basic_bullet_{side}', GL_TRIANGLES, 'bullets_mat'))
        bullet.add_component(Collider('bullets'))
        bullet.add_component(BulletScript(app.globals['BULLET_MOVE_SPEED'], 1))

        self.node.scene.new_light(PointLight(self.bullet_light_pos[side], 'orange', 1), bullet)

    def update(self, app):
        for reload_timer in self.reload_timers:
            self.reload_timers[reload_timer] += app.delta_time

        move_dir = 0
        if app.input.keys[pygame.K_a].held or app.input.keys[pygame.K_LEFT].held:
            move_dir += 1
        if app.input.keys[pygame.K_d].held or app.input.keys[pygame.K_RIGHT].held:
            move_dir -= 1

        x_pos = self.node.transform.local_position[0] + move_dir * app.delta_time * self.move_speed
        x_pos = min(self.max_x, max(self.min_x, x_pos))
        self.node.transform.set_local_position(
            (
                x_pos,
                self.node.transform.local_position[1],
                self.node.transform.local_position[2]
            )
        )

        if app.input.keys[pygame.K_m].held:
            self.shoot_bullet(app, 'left')
        if app.input.keys[pygame.K_k].held:
            self.shoot_bullet(app, 'right')
