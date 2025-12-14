from panda3d.core import TextNode
from .map import Map
from .utils import DrawText

class UserInterface:
    def __init__(self):
        self.map_window = Map(self)
        self.text_window = DrawText(
            parent = self.a2dTopLeft,
            text = "",
            fg = (1, 1, 1, 1),
        )

        self.taskMgr.add(self.screen_update, 'screen_update')

    def screen_update(self, task):
        self.map_window.update()
        
        position = self.player.position
        direction = self.player.direction
        velocity = self.player.velocity
        text = f'player x: {round(position[0], 1)}\n' \
            f'player y: {round(position[1], 1)}\n' \
            f'player z: {round(position[2], 1)}\n' \
            f'player angle: {int(direction[0])}\n' \
            f'player velocity x: {round(velocity[0], 1)}\n' \
            f'player velocity y: {round(velocity[1], 1)}\n' \
            f'player velocity z: {round(velocity[2], 1)}\n'
        self.text_window.setText(text)
        return task.cont