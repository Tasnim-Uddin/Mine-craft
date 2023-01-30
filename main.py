from ursina import Ursina, window, color, floor, lerp, time, Sky, Audio
from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrain import MeshTerrain
import random

app = Ursina()


window.borderless = True
window.fullscreen = False
window.exit_button.enabled = False
window.fps_counter.enabled = True
window.fullscreen = True

window.color = color.rgb(135, 206, 235)
sky = Sky()
sky.color = window.color

player = FirstPersonController()
player.gravity = 0.0
previous_x = player.x
previous_z = player.z

terrain = MeshTerrain()

count = 0

beginning_music = Audio('assets/audio/music/beginning.wav', loop=False, autoplay=False)
danny_music = Audio('assets/audio/music/danny.wav', loop=False, autoplay=False, volume=0.65)
living_mice_music = Audio('assets/audio/music/living_mice.wav', loop=False, autoplay=False)
mice_on_venus_music = Audio('assets/audio/music/mice_on_venus.wav', loop=False, autoplay=False)
sweden_music = Audio('assets/audio/music/sweden.wav', loop=False, autoplay=False)
minecraft_music = Audio('assets/audio/music/minecraft.wav', loop=False, autoplay=False)
wet_hands_music = Audio('assets/audio/music/wet_hands.wav', loop=False, autoplay=False, volume=0.75)

music = random.randrange(1, 8)
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
    global count, previous_x, previous_z

    count += 1
    if count == 2:
        # generate terrain at current chunk position
        terrain.generate_terrain()
        count = 0

    # change chunk position based on the player's current position
    if abs(player.x - previous_x) > 4 or abs(player.z - previous_z) > 4:
        previous_x = player.x
        previous_z = player.z
        terrain.chunk_generation.reset(previous_x, previous_z)

    block_found = False
    step = 2
    height = 1.4
    x = str(floor(player.x + 0.5))
    y = floor(player.y + 0.5)
    z = str(floor(player.z + 0.5))
    for i in range(-step, step):
        if terrain.terrain_dictionary.get(f'x{x}y{str(y + i)}z{z}') == 'terrain_present':
            target = y + i + height
            block_found = True
            break
    if block_found:
        player.y = lerp(player.y, target, 6 * time.dt)
    else:
        player.y -= 9.8 * time.dt


terrain.generate_terrain()


app.run()