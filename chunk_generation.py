from ursina import Vec2


class ChunkGeneration:
    """
    Chunks will generate in a swirl motion, going around the current chunk and then spiralling out,
    like a helix swirl of some sort
    """

    def __init__(self, chunk_width):
        self.chunk_width = chunk_width

        self.position = Vec2(0, 0)  # (x, z) tracks coordinates of chunk being generated

        self.reset(x=0, z=0)

        self.direction = [Vec2(0, 1),  # chunk loaded 1 above (in front) current chunk
                          Vec2(1, 0),  # then to the right
                          Vec2(0, -1),  # then down
                          Vec2(-1, 0)]  # then left

    def change_direction(self):
        if self.current_direction < 3:  # 3 diff possible chunk loading directions from index 0 to 3 (4 total if you look above)
            self.current_direction += 1
        else:
            self.current_direction = 0  # 0: reset to original chunk generation direction
            self.iteration += 1
        if self.current_direction < 2:
            self.run = (self.iteration * 2) - 1  # how many of the chunks in the same direction were generated for up and left (odd)
        else:
            self.run = self.iteration * 2   # how many of the chunks in the same direction were generated for right and down (even)

    def move(self):
        if self.count < self.run:
            self.position.x += self.direction[self.current_direction].x * self.chunk_width
            self.position.y += self.direction[self.current_direction].y * self.chunk_width  # y because in Vec2 the 2 components are (x, y) although it's technically (x, z)
            self.count += 1
        else:
            self.count = 0
            self.change_direction()
            self.move()

    def reset(self, x, z):
        self.position.x = x
        self.position.y = z
        self.run = 1
        self.iteration = 1
        self.count = 0
        self.current_direction = 0
