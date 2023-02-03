from ursina import Mesh, load_model, Vec2
from random_terrain_generation import RandomTerrainGeneration
from chunk_generation import ChunkGeneration
from mining_system import *
import random


class MeshTerrain:
    def __init__(self):
        self.block_model = load_model(name='block.obj', use_deepcopy=True)
        self.texture_atlas = 'texture_atlas.png'
        self.num_vertices = len(self.block_model.vertices)

        self.chunks = []
        self.chunk_num = 128
        self.chunk_width = 4  # Even because in generate_terrain(), distance is half of chunk_width on each side
        self.chunk_generation = ChunkGeneration(chunk_width=self.chunk_width)
        self.current_chunk = 0

        self.terrain_dictionary = {}
        self.vertices_dictionary = {}

        self.perlin = RandomTerrainGeneration()

        for i in range(0, self.chunk_num):
            block = Entity(model=Mesh(), texture=self.texture_atlas)
            block.texture_scale *= 64 / block.texture.width
            self.chunks.append(block)

    # highlight the nearest block that player is looking at
    def update(self, block_position, block_camera):
        highlight(block_position=block_position, block_camera=block_camera, terrain_dictionary=self.terrain_dictionary)

    def input(self, key):
        if (key == 'left mouse up') and highlighter.visible:
            block_centre = mine(terrain_dictionary=self.terrain_dictionary,
                                vertices_dictionary=self.vertices_dictionary, chunk=self.chunks)
            if block_centre is not None:
                self.generate_walls(centre=block_centre[0], chunk=block_centre[1])
                self.chunks[block_centre[1]].model.generate()

    # after mining to create sense of depth in hole
    def generate_walls(self, centre, chunk):
        if centre is None:
            return
        current_position = [Vec3(-1, 0, 0),
                            Vec3(1, 0, 0),
                            Vec3(0, -1, 0),
                            Vec3(0, 1, 0),
                            Vec3(0, 0, -1),
                            Vec3(0, 0, 1)]
        for face in range(0, 6):
            new_position = centre + current_position[face]
            if self.terrain_dictionary.get(f'x{str(floor(new_position.x))}'
                                           f'y{str(floor(new_position.y))}'
                                           f'z{str(floor(new_position.z))}') is None:
                self.generate_block(x=new_position.x, y=new_position.y, z=new_position.z, chunk=chunk, gap=False, block_type='soil')

    def generate_block(self, x, y, z, chunk='X', gap=True, block_type='grass'):
        if chunk == 'X':
            chunk = self.current_chunk
        model = self.chunks[chunk].model
        # gets all 36 vertices of a block and joins them to form a cube (creates a mesh not entity so faster to process)
        model.vertices.extend([Vec3(x, y, z) + vertex for vertex in self.block_model.vertices])
        # record terrain in the terrain dictionary
        self.terrain_dictionary[f'x{str(floor(x))}'
                                f'y{str(floor(y))}'
                                f'z{str(floor(z))}'] = 'terrain_present'
        # also record gap above this position to correct spawning walls around mined block after mining
        if gap:
            key = (f'x{str(floor(x))}'
                   f'y{str(floor(y + 1))}'
                   f'z{str(floor(z))}')
            if self.terrain_dictionary.get(key) is None:
                self.terrain_dictionary[key] = 'gap'
        # record chunk index and first vertex of current block in that chunk
        vertex = (chunk, len(model.vertices) - 37)
        self.vertices_dictionary[f'x{str(floor(x))}'
                                 f'y{str(floor(y))}'
                                 f'z{str(floor(z))}'] = vertex
        # texture_x and texture_y are the positions in the texture atlas for the block texture
        # horizontal: left to right is 8 to 16
        # vertical: top to bottom is 7 to 0
        texture_x = 8
        texture_y = 7
        if block_type == 'soil':
            texture_x = 9
            texture_y = 7
        elif block_type == 'stone':
            texture_x = 11
            texture_y = 7
        elif block_type == 'water':
            texture_x = 8
            texture_y = 6
        if random.random() > 0.86 and y < -4:
            # randomly place stone blocks
            texture_x = 11
            texture_y = 7
        # if high enough, use snow blocks instead of grass
        if y > 2:
            texture_x = 10
            texture_y = 7
        model.uvs.extend([Vec2(texture_x, texture_y) + face for face in self.block_model.uvs])
        model.generate()

    def generate_terrain(self):
        x = floor(self.chunk_generation.position.x)
        z = floor(self.chunk_generation.position.y)  # y because it's second component in Vec2(x, y)
        distance = int(self.chunk_width * 0.5)
        for current_x in range(-distance, distance):
            for current_z in range(-distance, distance):
                y = floor(self.perlin.get_height(x=x + current_x, z=z + current_z))
                if self.terrain_dictionary.get(f'x{str(floor(x + current_x))}'
                                               f'y{str(floor(y))}'
                                               f'z{str(floor(z + current_z))}') is None:
                    self.generate_block(x=x+current_x, y=y, z=z+current_z)
        self.chunks[self.current_chunk].model.generate()
        if self.current_chunk < self.chunk_num - 1:
            self.current_chunk += 1
        else:
            self.current_chunk = 0
        self.chunk_generation.move()
