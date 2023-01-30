from perlin_noise import PerlinNoise


class Perlin:
    def __init__(self):
        self.seed = 69420  # TODO make seeds accept string using ord()
        self.octaves = 2
        self.frequency = 64
        self.amplitude = 12

        self.perlin_noise = PerlinNoise(seed=self.seed, octaves=self.octaves)

    def get_height(self, x, z):
        y = self.perlin_noise([x / self.frequency, z / self.frequency]) * self.amplitude
        return y
