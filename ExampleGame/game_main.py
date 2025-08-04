import os
import sys
import pygame
sys.path.append(os.getcwd())

from Engine.app import App
from Engine.scene import Scene
from Engine.node import Node
from Engine.camera import Camera

from Engine.Lighting.point_light import PointLight

from Engine.components.render_mesh import RenderMesh
from Engine.components.ui.text_element import TextElement
from Engine.components.ui.button import Button
from Engine.components.ui.image import Image
from Engine.components.ui.box import Box
from Engine.components.ui.fill_box import FillBox

from Engine.materials.solid_image import SolidImage
from Engine.materials.blinn_phong_image import BlinnPhongImage
from Engine.materials.blinn_phong_solid import BlinnPhongSolid

from Engine.Utilities.window_properties import WindowProperties

from Components.Scripts.player_script import PlayerScript
from Components.Scripts.game_manager import GameManager

from OpenGL.GL import GL_TRIANGLES, GL_LINES


def play_button_clicked(app: App, button: Button) -> None:
    app.active_scene = app.scenes['main_scene']


def create_menu_scene(app: App):
    scene = Scene(app, 'main_menu')

    ui = Node(scene, 'ui')

    main_buttons_left_top = (100, 100)
    play_button_size = (200, 75)

    ui.add_component(
        Button(
            main_buttons_left_top,
            (100, 100, 100, 255),
            play_button_size,
            'left',
            'clicked',
            (play_button_clicked,)
        )
    )
    ui.add_component(
        TextElement(
            main_buttons_left_top,
            'Play',
            30
        )
    )

    ui.set_parent(scene)

    return scene

def create_main_scene(app: App):
    app.graphics_engine.new_mesh(f'{app.DIR}\\ExampleGame\\Assets\\SportsCar.obj', 'car')
    app.graphics_engine.new_mesh(f'{app.DIR}\\ExampleGame\\Assets\\space_ship.obj', 'ship')
    app.graphics_engine.new_mesh(f'{app.DIR}\\ExampleGame\\Assets\\mountains.obj', 'mountains')
    app.graphics_engine.new_mesh(f'{app.DIR}\\ExampleGame\\Assets\\bullets_1.obj', 'bullets')
    app.graphics_engine.new_mesh(f'{app.DIR}\\ExampleGame\\Assets\\basic_bullets.obj', 'basic_bullet_left', 'left')
    app.graphics_engine.new_mesh(f'{app.DIR}\\ExampleGame\\Assets\\basic_bullets.obj', 'basic_bullet_right', 'right')

    app.graphics_engine.new_material(BlinnPhongSolid('red'), 'red')
    app.graphics_engine.new_material(BlinnPhongSolid('teal'), 'teal')
    app.graphics_engine.new_material(BlinnPhongSolid('dark_navy'), 'dark_navy')
    app.graphics_engine.new_material(BlinnPhongSolid('orange', 0.8, 100), 'bullets_mat')
    app.graphics_engine.new_material(SolidImage(f'{app.DIR}\\ExampleGame\\Assets\\wood_2.webp'), 'wood')
    app.graphics_engine.new_material(BlinnPhongImage(f'{app.DIR}\\ExampleGame\\Assets\\wood_2.webp'), 'blinn_wood')
    app.graphics_engine.new_material(BlinnPhongSolid('navy'), 'blinn_navy')

    scene = Scene(app, 'main_scene')
    scene.camera = Camera((0, 5, -12), (0, -0.2, 1.75))

    scene.ambient_lighting = 0.5

    #scene.new_light(PointLight((4, 2, 8), 'red', 8))
    #scene.new_light(PointLight((-4, 2, 12), 'green', 5000))
    #scene.new_light(PointLight((0, 0, 0), 'purple', 15))

    MAX_X = 5
    MIN_X = -5

    MAX_Z = 40

    PLAYER_MOVE_SPEED = 5

    app.globals['BULLET_MOVE_SPEED'] = 10
    app.globals['ENEMY_MOVE_SPEED'] = 5
    app.globals['MAX_Z'] = MAX_Z

    app.add_singleton('GameManager', GameManager(MIN_X, MAX_X, MAX_Z), ('main_scene',))

    bottom_bar_height = 100
    bottom_border_weight = 10

    ui = Node(scene, 'ui')
    ui.add_component(
        Box(
            pygame.Rect(
                -bottom_border_weight,
                app.HEIGHT - bottom_bar_height + bottom_border_weight,
                app.WIDTH + bottom_border_weight * 2,
                bottom_bar_height + bottom_border_weight
            ),
            'dark_navy',
            bottom_border_weight,
            'blue_white'
        )
    )
    ui.add_component(
        Image(
            (app.WIDTH // 2 - bottom_bar_height // 2, app.HEIGHT - bottom_bar_height + bottom_border_weight),
            f'{app.DIR}\\ExampleGame\\Assets\\ship_image.png',
            (bottom_bar_height, bottom_bar_height)
        )
    )

    reload_bar_width = 25
    reload_bar_dist = 60

    reload_bar_left = ui.add_component(
        FillBox(
            pygame.Rect(
                app.WIDTH // 2 - reload_bar_dist - reload_bar_width / 2,
                app.HEIGHT - bottom_bar_height + bottom_border_weight + 20,
                reload_bar_width,
                bottom_bar_height * 0.6
            ),
            'green',
            'bottom',
            'red'
        ),
        'reload_bar_left'
    )
    reload_bar_right = ui.add_component(
        FillBox(
            pygame.Rect(
                app.WIDTH // 2 + reload_bar_dist - reload_bar_width / 2,
                app.HEIGHT - bottom_bar_height + bottom_border_weight + 20,
                reload_bar_width,
                bottom_bar_height * 0.6
            ),
            'green',
            'bottom',
            'red'
        ),
        'reload_bar_right'
    )

    ui.set_parent(scene)

    ship = Node(scene, 'ship')
    ship.transform.set_local_position((0, 0, 2))
    ship.transform.set_scale((0.2, 0.2, 0.2))
    ship.transform.set_eulers((0, 0, 180))
    ship.add_component(RenderMesh('ship', GL_TRIANGLES, 'teal'))
    ship.add_component(PlayerScript(MAX_X, MIN_X, PLAYER_MOVE_SPEED, reload_bar_left, reload_bar_right))
    ship.set_parent(scene)

    mountains_empty = Node(scene, 'mountains_empty')
    mountains_empty.transform.set_local_position((0, -1, 38))
    mountains_empty.set_parent(scene)

    mountains_lines = Node(scene, 'mountains_lines')
    mountains_lines.transform.set_local_position((0, 0.05, 0))
    mountains_lines.transform.set_scale((1, 1, 1))
    mountains_lines.transform.set_eulers((90, 90, 0))
    mountains_lines.add_component(RenderMesh('mountains', GL_LINES, 'teal'))
    mountains_lines.set_parent(mountains_empty)

    mountains_solid = Node(scene, 'mountains_solid')
    mountains_solid.transform.set_scale((1, 1, 1))
    mountains_solid.transform.set_eulers((90, 90, 0))
    mountains_solid.add_component(RenderMesh('mountains', GL_TRIANGLES, 'dark_navy'))
    mountains_solid.set_parent(mountains_empty)

    scene.new_light(PointLight((0, 20, -12), 'blue_white', 400), scene)
    scene.new_light(PointLight((0, 0, 1), 'blue', 5), ship)

    return scene


def main():
    window_props = WindowProperties()

    custom_colors = {
        'blue_white': (150, 150, 255, 255)
    }

    app = App(window_props, custom_colors)
    app.scenes['main_scene'] = create_main_scene(app)
    app.scenes['main_menu'] = create_menu_scene(app)
    app.active_scene = app.scenes['main_menu']
    app.run()


if __name__ == '__main__':
    main()
