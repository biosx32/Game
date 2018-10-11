from PIL import Image

import GameObjects


class GameMap():

	def load_map(self):
		img = Image.open(self.path)
		img = img.convert(mode='RGB')
		xs, ys = img.size
		self.size = xs // self.downscale, ys // self.downscale

		game_objects = []

		for i in range(xs):
			for j in range(ys):
				pixel = img.getpixel((i, j))

				if pixel == (0, 0, 0):
					Pos = GameObjects.V2(i // self.downscale , j // self.downscale)
					gmo = GameObjects.Basic(Pos, name='block', size=(self.block_size, self.block_size))
					game_objects.append(gmo)


		print("map loaded!")
		self.game_objects = game_objects

	def __init__(self, path, block_size, downscale=1):
		self.downscale = downscale
		self.size = None
		self.path = path
		self.block_size = block_size

		self.load_map()