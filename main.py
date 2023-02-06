from ursina import Ursina, window, color, floor, lerp, time, Sky, Audio, camera
from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrain import MeshTerrain
from snow_flake import SnowFlake
import random

app = Ursina()

window.borderless = True
window.fullscreen = False
window.exit_button.enabled = False
window.fps_counter.enabled = True
window.fullscreen = False

window.color = color.rgb(135, 206, 235)
sky = Sky()
sky.color = window.color

player = FirstPersonController()
player.cursor.visible = False
player.gravity = 0.0
previous_x = player.x
previous_z = player.z

terrain = MeshTerrain()

count = 0
snow_flake_num = 512

beginning_music = Audio(sound_file_name='assets/audio/music/beginning.mp3', loop=False, autoplay=False)
danny_music = Audio(sound_file_name='assets/audio/music/danny.mp3', loop=False, autoplay=False)
living_mice_music = Audio(sound_file_name='assets/audio/music/living_mice.mp3', loop=False, autoplay=False)
mice_on_venus_music = Audio(sound_file_name='assets/audio/music/mice_on_venus.mp3', loop=False, autoplay=False)
sweden_music = Audio(sound_file_name='assets/audio/music/sweden.mp3', loop=False, autoplay=False)
minecraft_music = Audio(sound_file_name='assets/audio/music/minecraft.mp3', loop=False, autoplay=False)
wet_hands_music = Audio(sound_file_name='assets/audio/music/wet_hands.mp3', loop=False, autoplay=False)
dry_hands_music = Audio(sound_file_name='assets/audio/music/wet_hands.mp3', loop=False, autoplay=False)

grass_footstep = Audio(sound_file_name='assets/audio/sounds/grass_footstep.mp3', loop=False, autoplay=False)
snow_footstep = Audio(sound_file_name='assets/audio/sounds/snow_footstep.mp3', loop=False, autoplay=False)

music = random.randrange(1, 9)
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
elif music == 8:
    dry_hands_music.play()


def input(key):
    terrain.input(key)
    if key == 'escape':
        exit()


def update():
    global count, previous_x, previous_z

    # generate terrain at current chunk position
    terrain.generate_terrain()
    count += 1
    if count == 2:
        count = 0
        # highlight the nearest looked at block within chunk range
        terrain.update(block_position=player.position, block_camera=camera)

    # change chunk position based on the player's current position
    if abs(player.x - previous_x) > 1 or abs(player.z - previous_z) > 1:
        previous_x = player.x
        previous_z = player.z
        terrain.chunk_generation.reset(x=previous_x, z=previous_z)
        if player.y > 4:
            if not snow_footstep.playing:
                snow_footstep.play()
        elif not grass_footstep.playing:
            grass_footstep.play()

    block_found = False
    step = 2
    height = 1.86
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

    for current in range(len(snow_flakes)):
        snow_flakes[current].physics(player_position=player.position)


snow_flakes = []
for i in range(snow_flake_num):
    current_snow_flake = SnowFlake(position=player.position)
    snow_flakes.append(current_snow_flake)

terrain.generate_terrain()

app.run()
