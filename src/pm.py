from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, CardMaker
from . import *
from .utils import DrawText

class PM(ShowBase, Lighting, UserInterface):
    def __init__(self, size):
        ShowBase.__init__(self)
        Lighting.__init__(self)

        self.properties = WindowProperties()
        self.properties.setTitle("Maze")
        self.properties.setSize(1200, 800)
        self.win.requestProperties(self.properties)
        self.setBackgroundColor(0.2, 0.5, 0.1)

        self.player = Player(self)
        self.maze = Maze(self, size)

        UserInterface.__init__(self)

        self.accept('escape', exit)
    
    def get(self, var):
        try:
            return getattr(self, var)
        except AttributeError:
            return None
        
    def set(self, var, val):
        setattr(self, var, val)

    def GAME_CLEAR(self):
        # クリアメッセージを表示
        self.clear_text = DrawText(
            parent = self.a2dTopCenter,
            text = "GAME CLEAR!",
            scale = 0.15,
            pos = (0, -0.5),
            fg = (1, 1, 0, 1),
            bg = (0, 0, 0, 0.5)
        )
        self.clear_screen = CardMaker('clear_screen')
        self.clear_screen.setFrameFullscreenQuad()
        clear_screen_node = self.render2d.attachNewNode(self.clear_screen.generate())
        clear_img = self.loader.loadTexture('textures/clear.png')
        clear_screen_node.setTexture(clear_img)