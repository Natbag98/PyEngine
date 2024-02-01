import os
import sys
sys.path.append(os.getcwd())

from main import App
from Engine.scene import Scene


def main():
    app = App()
    app.active_scene = Scene(app)
    app.run()


if __name__ == '__main__':
    main()
