import os
# カレントディレクトリの設定
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from math import *
from src import PM


class Game(PM):
    def __init__(self):
        # PMを継承する
        PM.__init__(self, 15)

game = Game()
game.run()