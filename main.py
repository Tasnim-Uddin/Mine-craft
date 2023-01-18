"""
Disclaimer: This solution is not scalable for creating a big world.
Creating a game like Minecraft requires specialized knowledge and is not as easy
to make as it looks.
You'll have to do some sort of chunking of the world and generate a combined mesh
instead of separate blocks if you want it to run fast. You can use the Mesh class for this.
You can then use blocks with colliders like in this example in a small area
around the player so that you can interact with the world.
"""

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

window.title = 'Superior Minecraft'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

grass = load_texture('assets/grass_block.png')
dirt = load_texture('assets/dirt_block.png')
stone = load_texture('assets/stone_block.png')
brick = load_texture('assets/brick_block.png')
hand = load_texture('assets/hand.png')
sky = load_texture('assets/sky.png')

punch_sound = Audio('assets/punch_sound', loop=False, autoplay=False)
background_music = Audio('assets/sweden', loop=True, autoplay=True)

block_pick = 1


# Define a Voxel class.
# By setting the parent to scene and the model to 'cube' it becomes a 3d button.


def update():
    global block_pick

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
            color=color.color(0, 0, random.uniform(0.9, 1.0)),
            highlight_color=color.lime,
            scale=0.5
        )

    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                punch_sound.play()
                if block_pick == 1:
                    voxel = Voxel(position=self.position + mouse.normal, texture=grass)
                if block_pick == 2:
                    voxel = Voxel(position=self.position + mouse.normal, texture=dirt)
                if block_pick == 3:
                    voxel = Voxel(position=self.position + mouse.normal, texture=stone)
                if block_pick == 4:
                    voxel = Voxel(position=self.position + mouse.normal, texture=brick)

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


for z in range(20):
    for x in range(20):
        voxel = Voxel(position=(x, 0, z))

player = FirstPersonController()
sky = Sky()
hand = Hand()

app.run()
