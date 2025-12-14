from direct.gui.DirectGui import OnscreenText
from panda3d.core import TextNode

class DrawText(OnscreenText):
    def __init__(self, parent=None, text='', font=None, scale=0.07, pos=(0.05, -0.1), fg=(0, 0, 0, 1), bg=(0, 0, 0, 0.1)):
        super().__init__(
            parent=parent,
            text=text,
            align=TextNode.ALeft,
            pos=pos,
            scale=scale,
            font=font,
            fg=fg,      # text color
            bg=bg,      # background color
            mayChange=True
        )
        self.star_time = None