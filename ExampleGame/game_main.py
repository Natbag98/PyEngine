import os
import sys
sys.path.append(os.getcwd())

from main import App
from Engine.scene import Scene
from Engine.node import Node
from Engine.components.render_mesh import RenderMesh

from OpenGL.GL import GL_TRIANGLES


def main():
    app = App()
    app.graphics_engine.new_mesh(f'{app.DIR}\\ExampleGame\\Assets\\SportsCar.obj', 'car')
    
    scene = Scene(app)
    car = Node(scene, 'car')
    car.transform.set_local_position((0, 0, 100))
    car.add_component(RenderMesh(car, 'car', GL_TRIANGLES, 'red'))
    car.set_parent(scene)

    app.active_scene = scene
    app.run()


if __name__ == '__main__':
    main()
