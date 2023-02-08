from ursina import Ursina, window, time, color, floor, lerp, Sky, Audio, camera
from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrain import MeshTerrain
from snow_flake import *
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
player_height = 1.7
player.cursor.visible = True
player.gravity = 0.0
player.normal_speed = player.speed
previous_x = player.x
previous_z = player.z

terrain = MeshTerrain()
# snow = Snowfall(player)
generating_terrain = True

cow = Entity(model='assets/models/cow.obj', texture='assets/textures/mobs/cow.png')
cow.position = player.position + player.forward * 7

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


for i in range(128):
    terrain.generate_terrain()


def input(key):
    global generating_terrain

    terrain.input(key)

    if key == 'escape':
        exit()

    if key == 'control':
        player.speed = player.normal_speed * 1.5

    if key == 'control up':
        player.speed = player.normal_speed

    if key == 'g':
        generating_terrain = not generating_terrain


def update():
    global previous_x, previous_z

    # highlight the nearest looked at block within chunk range
    terrain.update(block_position=player.position, block_camera=camera)

    count = 0
    count += 1
    if count == 4:
        count = 0
        # generate terrain at current chunk position
        if generating_terrain:
            for _ in range(4):
                terrain.generate_terrain()

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

    # auto jump
    block_found = False
    step = 2
    x = floor(player.x + 0.5)
    y = floor(player.y + 0.5)
    z = floor(player.z + 0.5)
    for i in range(-step, step):
        if terrain.terrain_dictionary.get((x, y + i, z)) == 'terrain_present':
            if terrain.terrain_dictionary.get((x, y + i + 1, z)) == 'terrain_present':
                target = y + i + 1 + player_height
                block_found = True
                break
            target = y + i + player_height
            block_found = True
            break
    if block_found:
        player.y = lerp(player.y, target, 6 * time.dt)
    else:
        player.y -= 9.8 * time.dt


app.run()
