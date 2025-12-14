from panda3d.core import PandaNode, Point3, CardMaker
from random import shuffle
from math import floor

class Maze:
    def __init__(self, base, maze_size = 35):
        self.base = base
        self.maze_size = maze_size
        if self.maze_size % 2 == 0: self.maze_size += 1  # １辺の長さは奇数である必要がある
                
        self.base.maze_node = self.base.render.attachNewNode(PandaNode('maze_node'))
        self.wall_model = self.base.loader.loadModel('models/BirchTree')
        self.wall_model.setScale(0.25)

        self.maze_list = self.create_maze(self.maze_size)
        self.show_maze(self.maze_list)
        
        ground_card = CardMaker('ground_card')
        ground_card.setFrame(   # カードの大きさ指定
            0,
            maze_size,
            0,
            maze_size
        )
        ground_card.setUvRange(     # カードにテクスチャを繰り返し貼り付け    
            (0, 0),
            (maze_size, maze_size)
        )
        ground = self.base.render.attachNewNode(ground_card.generate())
        ground.setP(-90)
        ground.setZ(-0.01)
        grass_texture = self.base.loader.loadTexture("models/maps/envir-ground.jpg")
        ground.setTexture(grass_texture)

        start_card = CardMaker('start_card')
        start_card.setFrame(0, 1.5, 0, 1.5)
        start = self.base.render.attachNewNode(start_card.generate())
        start.setH(180)
        start.setPos(2, 0, 0.5)
        start_texture = self.base.loader.loadTexture('textures/13.png')
        start.setTexture(start_texture)

        goal_card = CardMaker('goal_card')
        goal_card.setFrame(0, 1.5, 0, 1.5)
        goal = self.base.render.attachNewNode(goal_card.generate())
        goal.setPos(maze_size-2.5, maze_size, 0.5)
        goal_texture = self.base.loader.loadTexture('textures/03.png')
        goal.setTexture(goal_texture)

    def create_maze_list(self, maze_size:int):
        '''
        通路を0, 壁を1で表記した二次元リストを返す
        棒倒し法による迷路の作成
        参考：https://algoful.com/Archive/Algorithm/MazeBar
        '''
        size = maze_size
        
        maze = [[0] * size for _ in range(size)]
        # 初期化
        for y in range(size):
            for x in range(size):
                if y == 0 or y == size - 1 or x == 0 or x == size - 1:
                    # 外周を壁にする
                    maze[y][x] = 1
                elif x % 2 == 0 and y % 2 == 0:
                    # 内部に柱を設置
                    maze[y][x] = 1

        # 柱を倒す
        for y in range(2, size - 1, 2):
            for x in range(2, size - 1, 2):
                # 倒す方向の候補 [dx, dy]
                directions = [[0, 1], [1, 0], [-1, 0]]

                # 一行目（y=2）の柱のみ、上方向 [0, -1] を含める
                if y == 2: directions.append([-1, 0])

                # ランダムに並び替え
                shuffle(directions)
                
                while directions:
                    dx, dy = directions.pop()
                    # 柱の隣（倒す先のマス）の座標
                    nx, ny = x + dx, y + dy
                    if not maze[ny][nx]:    # 壁でなければ、壁にする
                        maze[ny][nx] = 1
                        break
        
        # スタートとゴールを作成
        maze[0][1] = 0
        maze[size-1][size-2] = 0

        return maze
    
    def add_maze_model(self, x, y):
        key = f'{x}_{y}'
        self.base.set(key, self.base.maze_node.attachNewNode(PandaNode(key)))
        placeholder = self.base.get(key)
        placeholder.setPos(x, y, 0)
        
        wall1 = placeholder.attachNewNode(PandaNode("wall1"))
        wall1.setPos(0, 0, 0)
        self.wall_model.instanceTo(wall1)

        wall2 = placeholder.attachNewNode(PandaNode("wall2"))
        wall2.setPos(0.5, 0, 0)
        self.wall_model.instanceTo(wall2)

        wall3 = placeholder.attachNewNode(PandaNode("wall3"))
        wall3.setPos(0, 0.5, 0)
        self.wall_model.instanceTo(wall3)

        wall4 = placeholder.attachNewNode(PandaNode("wall4"))
        wall4.setPos(0.5, 0.5, 0)
        self.wall_model.instanceTo(wall4)

        
    def create_maze(self, maze_size):
        maze_list = self.create_maze_list(maze_size)
        for y in range(maze_size):
            for x in range(maze_size):
                if maze_list[y][x]:
                    self.add_maze_model(x, y)
        return maze_list

    def show_maze(self, maze_list):
        print('Created maze is shown below.')
        print()
        for i in range(self.maze_size-1, -1, -1):
            t = ''
            for m in maze_list[i]:
                if m: t+= "+"
                else: t+= " "
            print(t)
        print()
    
    def is_wall_at(self, x, y):
        x, y = floor(x), floor(y)
        key = f'{x}_{y}'
        if self.base.get(key):
            return True
        else:
            return False
