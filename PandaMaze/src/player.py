from math import *
from direct.actor.Actor import Actor
from panda3d.core import Point3, VBase3, Vec3, PandaNode
from direct.showbase.ShowBaseGlobal import globalClock
from .camera import Camera

class Player(Camera):
    angular_velocity = 250  # 回転速度
    speed = 1               # 移動速度
    margin = Point3(0.2, 0.2, 0)
    
    def __init__(self, base):
        self.base = base
        self.base.player_node = self.base.render.attachNewNode(PandaNode('player_node'))
        
        self.model = Actor(
            'models/panda', 
            {'walk': 'models/panda-walk'}
            )
        self.model.play('walk', fromFrame = 1, toFrame = 2) # 1歩だけ歩いて停止
        self.isWalking = False

        self.model.setScale(0.08)
        self.base.player_model_node = self.base.player_node.attachNewNode(PandaNode('player_model_node'))
        self.model.reparentTo(self.base.player_model_node)

        Camera.__init__(self)

        self.rotate_state = None
        self.target_angle = 180

        self.moving_state = False
        self.target_x = 1
        self.target_y = 0

        self.position = Point3(self.target_x, self.target_y, 0)
        self.direction = VBase3(self.target_angle, 0, 0)
        self.velocity = Vec3(0, 0, 0)

        # キー操作の保存
        self.key_map = {
            'arrow_up': 0,
            'arrow_down': 0,
            'arrow_right': 0,
            'arrow_left': 0,
            'z': 0,
        }

        # ユーザー操作
        self.base.accept('arrow_up', self.update_key_map, ['arrow_up', 1])
        self.base.accept('arrow_down', self.update_key_map, ['arrow_down', 1])
        self.base.accept('arrow_right', self.update_key_map, ['arrow_right', 1])
        self.base.accept('arrow_left', self.update_key_map, ['arrow_left', 1])
        self.base.accept('arrow_up-up', self.update_key_map, ['arrow_up', 0])
        self.base.accept('arrow_down-up', self.update_key_map, ['arrow_down', 0])
        self.base.accept('arrow_right-up', self.update_key_map, ['arrow_right', 0])
        self.base.accept('arrow_left-up', self.update_key_map, ['arrow_left', 0])
        # debug用
        self.base.accept('z', self.update_key_map, ['z', 1])
        self.base.accept('z-up', self.update_key_map, ['z', 0])

        self.base.taskMgr.add(self.player_update, 'player_update')

    def update_key_map(self, key_name, key_state):
        self.key_map[key_name] = key_state
    
    def update_direction(self):
        """
            右か左が押されると９０度回転
        """
        # 移動中は操作を受け付けない
        if self.moving_state: return

        # 動いていないときに角度の補正
        if not self.isWalking:
            if self.target_angle > 360 or self.target_angle < 0:
                self.target_angle %= 360
                self.direction.x = self.target_angle
        
        if not self.rotate_state:
            # 回転していない
            key_map = self.key_map
            right = key_map['arrow_right']
            left = key_map['arrow_left']
            if left == right: return
            if right:
                self.rotate_state = "Right"
                self.target_angle -= 90
            else:
                self.rotate_state = "Left"
                self.target_angle += 90
        dt = globalClock.getDt()
        target_angle = self.target_angle
        if self.rotate_state == "Right":
            # 右回転中
            angle = self.direction.x - Player.angular_velocity * dt
            if angle <= target_angle:    # 回転しすぎ
                angle = target_angle
                self.rotate_state = None
        elif self.rotate_state == "Left":
            # 左回転中
            angle = self.direction.x + Player.angular_velocity * dt
            if angle >= target_angle:
                angle = target_angle
                self.rotate_state = None
        self.direction = VBase3(angle, 0, 0)
    
    def update_velocity(self):
        """
            速度を更新
        """
        if not self.moving_state:
            # 移動していない
            key_map = self.key_map
            up = key_map['arrow_up']
            down = key_map['arrow_down']
            if up == down: return

            # 移動方向と目標位地の補正
            angle = self.direction.x
            velocity = Vec3(
                round(cos(radians(angle-90))),
                round(sin(radians(angle-90))),
                key_map['z']    # for debug
            ) * (up - down)
            target_x = self.target_x + velocity.x
            target_y = self.target_y + velocity.y
            
            if target_y >= self.base.maze.maze_size:
                self.base.GAME_CLEAR()
                return

            # 移動先が壁でなければ移動開始
            if not self.base.maze.is_wall_at(target_x, target_y) and target_y >= 0:
                self.target_x = int(target_x)
                self.target_y = int(target_y)
                self.velocity = velocity * Player.speed
                self.moving_state = True
        
        # 目標地点に到達していたら停止
        flag = False
        if self.velocity.x > 0:
            if self.position.x >= self.target_x:
                flag = True
        elif self.velocity.x < 0:
            if self.position.x <= self.target_x:
                flag = True
        if self.velocity.y > 0:
            if self.position.y >= self.target_y:
                flag = True
        elif self.velocity.y < 0:
            if self.position.y <= self.target_y:
                flag = True
        if flag:
            self.position.x = self.target_x
            self.position.y = self.target_y
            self.velocity = Vec3(0, 0, 0)
            self.moving_state = None

    def update_position(self):
        '''
            上か下が押されると1マス動く
        '''
        if self.rotate_state: return    # 回転中は操作を受け付けない

        self.update_velocity()
        dt = globalClock.getDt()
        self.position = self.position + self.velocity * dt

    def draw(self):
        self.base.player_model_node.setH(self.direction.x)
        # self.change_position_when_interfering_with_wall()
        self.base.player_node.setPos(self.position + Player.margin)
        
        # Animation
        if self.moving_state or self.rotate_state:
            if not self.isWalking:
                self.model.loop("walk", fromFrame=self.model.getCurrentFrame())
                self.isWalking = True
        elif self.isWalking:
            self.model.stop()
            self.isWalking = False
    
    def player_update(self, task):
        self.update_direction()
        self.update_position()
        self.draw()
        return task.cont
    
    # 移動先が壁でないか判定
    def check_if_next_position_is_wall(self, target_x, target_y):
        self.base.maze.is_wall_at(target_x, target_y)
    
    # 衝突判定（今は使ってない）
    def change_position_when_interfering_with_wall(self):
        vx, vy, _ = self.velocity
        x, y, _ = self.position

        # x軸方向の干渉チェック
        if 0 < vx:      # x軸方向への移動中
            x_to_check = x + 1
            if self.base.maze.is_wall_at(x_to_check, y):
                x = floor(x_to_check) - 0.8
        elif vx < 0:
            x_to_check = x
            if self.base.maze.is_wall_at(x_to_check, y):
                x = floor(x_to_check) + 1
        
        # y軸方向の干渉チェック
        if 0 < vy:      # y軸方向への移動中
            y_to_check = y + 1
            if self.base.maze.is_wall_at(x, y_to_check):
                y = floor(y_to_check) - 0.8
        elif vy < 0:
            y_to_check = y
            if self.base.maze.is_wall_at(x, y_to_check):
                y = floor(y_to_check) + 1
        self.position = Point3(x, y, 0)