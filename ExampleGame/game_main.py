import os
import sys
sys.path.append(os.getcwd())

from main import App
from Engine.scene import Scene


if __name__ == '__main__':
    game = App()
    game.active_scene = Scene(game)
    game.run()
