from ursina import Entity, color, floor, Vec3

highlighter = Entity(model='block.obj', color=color.rgba(1, 1, 0, 0.4))
highlighter.scale = 1.001  # so that the highlighted block isn't directly on the face of the actual block, but slightly bigger
player_height = 1.7


def highlight(block_position, block_camera, terrain_dictionary):
    for i in range(1, 32):  # goes from current camera position and shoots out and if it finds a block within that range then it highlights is (so selects it)
        current_position = block_position + Vec3(0, player_height, 0) + block_camera.forward * (i*0.5)  # adjust highlighter for player's height
        # TODO fix to make it 100% accurate
        x = round(current_position.x)
        y = floor(current_position.y)
        z = round(current_position.z)
        highlighter.x = x
        highlighter.y = y
        highlighter.z = z
        if terrain_dictionary.get((x, y, z)) == 'terrain_present':
            highlighter.visible = True
            break
        else:
            highlighter.visible = False


def mine(terrain_dictionary, vertices_dictionary, chunk):
    if not highlighter.visible:
        return
    current_vertex = vertices_dictionary.get((floor(highlighter.x), floor(highlighter.y), floor(highlighter.z)))
    # check if block is highlighted and if not then don't mine
    if current_vertex is None:
        return
    for vertex in range(current_vertex[1] + 1, current_vertex[1] + 37):
        # looks for the block's vertex at that chunk and iterates through each vertex of that block in the chunk and gets the y position of the block vertex. it then changes the y position to +999 so it appears as if it has disappeared or block is mined
        chunk[current_vertex[0]].model.vertices[vertex][1] += 999999

    chunk[current_vertex[0]].model.generate()

    terrain_dictionary[(floor(highlighter.x), floor(highlighter.y), floor(highlighter.z))] = 'gap'
    vertices_dictionary[(floor(highlighter.x), floor(highlighter.y), floor(highlighter.z))] = None

    return highlighter.position, current_vertex[0]
