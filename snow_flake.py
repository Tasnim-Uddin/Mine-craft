from ursina import Entity, time
import random


class SnowFlake(Entity):
    def __init__(self, position):
        super().__init__(model='quad', texture='snow_flake.png', position=position, double_sided=True, scale=0.2)
        self.x += random.random() * 40 - 20
        self.y += random.random() * 10 + 5
        self.z += random.random() * 40 - 20
        min_speed = 0.6
        self.fall_speed = random.random() * 4 + min_speed
        self.rotation_speed = random.random() * 4

    def physics(self, player_position):
        self.y -= self.fall_speed * time.dt
        self.rotation_y += self.rotation_speed * time.dt
        if self.y < 0:
            self.x += player_position.x + random.random() * 40 - 20
            self.y += player_position.y + random.random() * 10 + 5
            self.z += player_position.z + random.random() * 40 - 20
            # TODO change to make it check if hits terrain block