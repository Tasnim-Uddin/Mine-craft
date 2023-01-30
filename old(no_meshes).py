from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
# from mesh_terrain import MeshTerrain
from numpy import floor
from perlin_noise import PerlinNoise
import random

app = Ursina()

window.title = 'Cave Game'
window.borderless = True
window.fullscreen = False
window.exit_button.enabled = False
window.fps_counter.enabled = True

window.color = color.rgb(135, 206, 235)
scene.fog_color = color.rgb(191, 198, 201)
scene.fog_density = 0.03

terrain_width = 32

block_model = 'assets/models/block_model.obj'
hand_model = 'assets/models/hand_model.obj'

grass = 'assets/textures/grass_block.png'
dirt = 'assets/textures/dirt_block.png'
stone = 'assets/textures/stone_block.png'
brick = 'assets/textures/brick_block.png'
hand_texture = 'assets/textures/hand.png'
sky = 'assets/textures/sky.png'

punch_sound = Audio('assets/audio/sounds/block_sound.wav', loop=False, autoplay=False)

beginning_music = Audio('assets/audio/music/beginning.wav', loop=False, autoplay=False)
danny_music = Audio('assets/audio/music/danny.wav', loop=False, autoplay=False, volume=0.65)
living_mice_music = Audio('assets/audio/music/living_mice.wav', loop=False, autoplay=False)
mice_on_venus_music = Audio('assets/audio/music/mice_on_venus.wav', loop=False, autoplay=False)
sweden_music = Audio('assets/audio/music/sweden.wav', loop=False, autoplay=False)
minecraft_music = Audio('assets/audio/music/minecraft.wav', loop=False, autoplay=False)
wet_hands_music = Audio('assets/audio/music/wet_hands.wav', loop=False, autoplay=False, volume=0.75)

block_pick = 1

noise = PerlinNoise(octaves=2, seed=2023)
amplifier = 6
frequency = 24

player = FirstPersonController()
player.gravity = 0.5
player.normal_speed = player.speed
player.jump_height = 1.5

# music = random.randrange(1, (len('assets/audio/music')) + 1)
music = 7
if music == 1:
    beginning_music.play()
elif music == 2:
    danny_music.play()
elif music == 3:
    living_mice_music.play()
elif music == 4:
    mice_on_venus_music.play()
elif music == 5:
    sweden_music.play()
elif music == 6:
    minecraft_music.play()
elif music == 7:
    wet_hands_music.play()


def update():
    global block_pick

    if held_keys['escape']:
        quit()

    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()

    if held_keys['1']:
        block_pick = 1
    if held_keys['2']:
        block_pick = 2
    if held_keys['3']:
        block_pick = 3
    if held_keys['4']:
        block_pick = 4


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=grass):
        super().__init__(
            parent=scene,
            position=position,
            model=block_model,
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, 1),
            highlight_color=color.lime,
            scale=0.5
        )

    def input(self, key):
        if key == 'control':
            player.speed = player.normal_speed * 1.5
        if key == 'control up':
            player.speed = player.normal_speed

        if self.hovered:
            if key == 'right mouse down':
                punch_sound.play()
                if block_pick == 1:
                    placed_block = Voxel(position=self.position + mouse.normal, texture=grass)
                if block_pick == 2:
                    placed_block = Voxel(position=self.position + mouse.normal, texture=dirt)
                if block_pick == 3:
                    placed_block = Voxel(position=self.position + mouse.normal, texture=stone)
                if block_pick == 4:
                    placed_block = Voxel(position=self.position + mouse.normal, texture=brick)

            if key == 'left mouse down':
                punch_sound.play()
                destroy(self)


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=sky,
            scale=150,
            double_sided=True
        )


# sky = Sky()  TODO


class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model=hand_model,
            texture=hand_texture,
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.6, -0.6)
        )

    def active(self):
        self.position = Vec2(0.5, -0.55)

    def passive(self):
        self.position = Vec2(0.6, -0.6)


hand = Hand()

for x in range(terrain_width):
    for z in range(terrain_width):
        block = Voxel(position=(x, floor(noise([x / frequency, z / frequency]) * amplifier), z))


app.run()
