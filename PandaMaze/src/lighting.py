from panda3d.core import AmbientLight, DirectionalLight, Vec3, Vec4

class Lighting:
    def __init__(self):
        # 環境光
        environment_light = AmbientLight("environment_light")
        environment_light.setColor(Vec4(0.5, 0.5, 0.5, 1))
        self.environment_light_node = self.render.attachNewNode(environment_light)
        self.render.setLight(self.environment_light_node)

        # 指向性光源
        directional_light = DirectionalLight('directional_light')
        directional_light.setDirection(Vec3(1, 1, -1))
        directional_light.setColor(Vec4(0.8, 0.8, 0.8, 1))
        self.directional_light_node = self.render.attachNewNode(directional_light)
        self.render.setLight(self.directional_light_node)