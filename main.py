from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor
from perlin_noise import PerlinNoise


app = Ursina()


window.title = 'Superior Minecraft'
window.borderless = False
window.fullscreen = False
window.exit_button.enabled = False
window.fps_counter.enabled = True

terrain_width = 32

grass = load_texture('assets/grass_block.png')
dirt = load_texture('assets/dirt_block.png')
stone = load_texture('assets/stone_block.png')
brick = load_texture('assets/brick_block.png')
hand = load_texture('assets/hand.png')
sky = load_texture('assets/sky.png')

punch_sound = Audio('assets/punch_sound', loop=False, autoplay=False)
background_music = Audio('assets/sweden', loop=True, autoplay=True)

block_pick = 1

noise = PerlinNoise(octaves=1, seed=2025)
amplifier = 6
frequency = 24


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
            model='assets/block_model',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, 1),
            highlight_color=color.lime,
            scale=0.5
        )

    def input(self, key):
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


class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='assets/hand_model',
            texture=hand,
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.6, -0.6)
        )

    def active(self):
        self.position = Vec2(0.5, -0.55)

    def passive(self):
        self.position = Vec2(0.6, -0.6)


for z in range(terrain_width):
    for x in range(terrain_width):
        block = Voxel(position=(x, floor(noise([x/frequency, z/frequency]) * amplifier), z))

player = FirstPersonController()
sky = Sky()
hand = Hand()

app.run()
