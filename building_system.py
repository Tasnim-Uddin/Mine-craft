from ursina import floor, Vec3


def check_building_possible(build_site, terrain_dictionary):
    x = floor(build_site.x)
    y = floor(build_site.y + 1)  # add 1 because actual build site 1 block above the block you are looking at
    z = floor(build_site.z)

    if (terrain_dictionary.get((x, y, z)) != 'gap') and (terrain_dictionary.get((x, y, z)) is not None):
        return None

    return Vec3(x, y, z)


def gap_wall(terrain_dictionary, build_site):
    current_position = [Vec3(-1, 0, 0),
                        Vec3(1, 0, 0),
                        Vec3(0, -1, 0),
                        Vec3(0, 1, 0),
                        Vec3(0, 0, -1),
                        Vec3(0, 0, 1)]
    for face in range(0, 6):
        new_position = build_site + current_position[face]
        if terrain_dictionary.get((floor(new_position.x), floor(new_position.y), floor(new_position.z))) is None:
            terrain_dictionary[(floor(new_position.x), floor(new_position.y), floor(new_position.z))] = 'gap'
