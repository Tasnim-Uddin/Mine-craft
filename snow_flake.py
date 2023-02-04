from ursina import Entity, time
import random


class SnowFlake(Entity):
    player = None

    @staticmethod  # so this isn't created for every instance of the class (so all snowflakes have the same one)
    def set_player(player_entity):
        SnowFlake.player = player_entity

    def __init__(self, position):
        super().__init__(model='quad', texture='snow_flake.png', position=position, double_sided=True, scale=0.2)
        self.x += random.random() * 20 - 10
        self.y += random.random() * 10 + 5
        self.z += random.random() * 20 - 10
        min_speed = 0.6
        self.fall_speed = random.random() * 4 + min_speed
        min_rotation = 100
        self.rotation_speed = random.random() * 40 + min_rotation

    def update(self):
        self.physics()

    def physics(self):
        player_position = SnowFlake.player.position
        self.y -= self.fall_speed * time.dt
        self.rotation_y += self.rotation_speed * time.dt
        if self.y < 0:  # TODO change to make it check if hits terrain block
            self.x = player_position.x + (random.random() * 20 - 10)
            self.y += player_position.y + (random.random() * 10 + 5)
            self.z = player_position.z + (random.random() * 20 - 10)


class Snowfall:
    def __init__(self, player_reference):
        self.snow_flakes = []
        SnowFlake.set_player(player_reference)
        for i in range(128):
            current_snow_flake = SnowFlake(player_reference.position)
            self.snow_flakes.append(current_snow_flake)