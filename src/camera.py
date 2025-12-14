from math import *
from panda3d.core import Vec3, PerspectiveLens
class Camera:
    far_length = 10     # カメラの遠方クリップ面までの距離
    camera_back = 1.4
    camera_height = 1.5
    camera_forward = 1
    base_camera_near = 0.5
    player_camera_near = 0.1
    cam_fov = 80

    def __init__(self):
        # マウス操作の禁止
        self.base.disableMouse()

        # base cam
        self.base.cam.reparentTo(self.base.player_node)
        self.base.camLens.setFov(Camera.cam_fov)
        self.base.camLens.setFar(Camera.far_length)
        self.base.camLens.setNear(Camera.base_camera_near)
        self.base.cam.setPos(
            Vec3(0, -Camera.camera_back, Camera.camera_height)
        )
        self.base.cam.lookAt(
            Vec3(0, Camera.camera_forward, Camera.camera_height-1)
        )

        # player cam
        player_cam_lens = PerspectiveLens()
        player_cam_lens.setFov(Camera.cam_fov)
        player_cam_lens.setNear(Camera.player_camera_near)
        player_cam_lens.setFar(Camera.far_length)
        self.player_cam = self.base.makeCamera(self.base.win)
        self.player_cam.node().setLens(player_cam_lens)
        self.player_cam.reparentTo(self.base.player_model_node)
        self.player_cam.setPos(
            Vec3(0, 0, Camera.camera_height)
        )
        self.player_cam.setH(180)

        # カメラのリストとアクティブなカメラのインデックス
        self.base.cameras = [self.base.cam, self.player_cam]
        self.base.active_cam = 0
        self.base.cameras[1].node().getDisplayRegion(0).setActive(False)

        # カメラの切り替え
        self.base.accept("t", self.toggle_cam)

    def toggle_cam(self):
        self.base.cameras[self.base.active_cam].node().getDisplayRegion(0).setActive(False)
        self.base.active_cam = (self.base.active_cam + 1) % len(self.base.cameras)
        self.base.cameras[self.base.active_cam].node().getDisplayRegion(0).setActive(True)

    
