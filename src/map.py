from direct.gui.DirectGui import OnscreenImage
from panda3d.core import TransparencyAttrib

class MapSprite(OnscreenImage):
    tex_dict = {
        'unknown': '00',
        'wall': '01',
        'path_panda': '02',
        'goal_panda': '03',
        'path': '10',
        'start': '11',
        'goal': '12',
        'start_panda': '13',
    }
    def __init__(self, parent = None, image = 'unknown', x = 0, y = 0):
        super().__init__(
            parent=parent,
            image=f'textures/{MapSprite.tex_dict[image]}.png',
            pos=(x, 0, y),
            scale=(1/2, 1/2, 1/2)
        )
        self.state = image

    def update_image(self, image):
        if self.state != image:
            self.setImage(f'textures/{MapSprite.tex_dict[image]}.png')
            self.state = image

class Map:
    '''
    ミニマップを表示・更新するクラス
    '''
    diff = [-1, 0, 1]  # 上下左右の差分座標
    
    def __init__(self, base):
        self.base = base
        self.size = self.base.maze.maze_size
        self.base.map_node = self.base.render2d.attachNewNode('map_node')
        self.base.map_node.setPos(0.5, 0, -0.9)
        self.base.map_node.setScale(1/self.size/2, 1, 3/self.size/4)
        self.base.map_node.setTransparency(TransparencyAttrib.MAlpha)
        self.base.map_node.setAlphaScale(0.7)
        self.img_list = [[None] * self.size for _ in range(self.size)]
        for y in range(self.size):
            for x in range(self.size):
                self.img_list[y][x] = MapSprite(
                        parent=self.base.map_node,
                        image = 'unknown',
                        x = x,
                        y = y
                    )
        self.update(self.size-2, self.size-1, False) # ゴールを表示
        self.update()

    def update_map(self, x, y, panda = False, mode = 'show'):
        if mode == 'show':
            ml = self.base.maze.maze_list
            if ml[y][x] == 1:
                self.img_list[y][x].update_image('wall')
            else:
                if (x, y) == (1, 0):
                    img_name = 'start'
                elif (x, y) == (self.size - 2, self.size - 1):
                    img_name = 'goal'
                else:
                    img_name = 'path'
                if panda:
                    img_name += '_panda'
                self.img_list[y][x].update_image(img_name)
        else:
            self.img_list[y][x]('unknown')

    def update(self, px = 0, py = 0, panda = True):
        if not px: px = self.base.player.target_x
        if not py: py = self.base.player.target_y
        self.update_map(px, py, panda=panda)
        for dy in Map.diff:
            for dx in Map.diff:
                if dx == 0 and dy == 0:
                    continue
                nx = px + dx
                ny = py + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    self.update_map(nx, ny)