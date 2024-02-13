import os
import sys
sys.path.append(os.getcwd())

from main import App
from Engine.scene import Scene
from Engine.node import Node
from Engine.components.render_mesh import RenderMesh
from Engine.materials.solid_color import SolidColor
from Engine.materials.solid_image import SolidImage

from Components.Scripts.spin_script import SpinScript

from OpenGL.GL import GL_TRIANGLES


def main():
    app = App()

    app.graphics_engine.new_mesh(f'{app.DIR}\\ExampleGame\\Assets\\SportsCar.obj', 'car')
    app.graphics_engine.new_mesh(f'{app.DIR}\\ExampleGame\\Assets\\space_ship.obj', 'ship')

    app.graphics_engine.new_material(SolidColor('red'), 'red')
    app.graphics_engine.new_material(SolidImage(f'{app.DIR}\\ExampleGame\\Assets\\wood.jpeg'), 'wood')

    scene = Scene(app)

    car = Node(scene, 'car')
    car.transform.set_local_position((-2, 0, 10))
    car.transform.set_eulers((0, 0, 90))
    car.add_component(RenderMesh('car', GL_TRIANGLES, 'red'))
    car.add_component(SpinScript(1))
    car.set_parent(scene)

    ship = Node(scene, 'ship')
    ship.transform.set_local_position((2, 0, 10))
    ship.transform.set_scale((0.5, 0.5, 0.5))
    ship.add_component(RenderMesh('ship', GL_TRIANGLES, 'wood'))
    ship.add_component(SpinScript(1))
    ship.set_parent(scene)

    app.active_scene = scene
    app.run()


if __name__ == '__main__':
    main()
