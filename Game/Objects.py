from PIL import Image
from Game.Low import V2


class Animation:
	def __init__(self, image_list, range=None):
		if not range:
			range = 0, len(list)
		self.range = range
		self.index = range[0]
		self.image_list = image_list

	def __iter__(self):
		self.index = range[0]
		return self

	def __next__(self):
		self.index += 1

		if self.index == range[1]:
			self.index = range[0]


class GameObject:
	_id_counter = {}

	def __init__(self, pos, tname=None):
		if not pos:
			pos = V2(0, 0)

		self._collisionCheck = False
		self.pos = pos
		self.tname = tname

		if not tname in self._id_counter:
			self._id_counter[tname] = 0

		self.ID = self._id_counter[tname]
		self._id_counter[tname] += 1

	def __str__(self):
		return "{}:{} at {}".format(self.tname, self.ID, self.pos)

	def __repr__(self):
		return str(self)


class Block(GameObject):
	def __init__(self, pos):
		super().__init__(pos, tname='block')


class Player(GameObject):
	def __init__(self, pos):
		super().__init__(pos, tname='player')
		self.type = 'player'


class Camera(GameObject):
	def __init__(self, pos=None):
		pos = pos or V2(0, 0)
		super().__init__(pos, tname='camera')
		self.type = 'player'


class GameMap:

	def load_map(self):
		img = Image.open(self.path).convert(mode='RGB')
		self.size = (V2(img.size) / self.downscale).to_integer()

		for i in range(self.size.x):
			for j in range(self.size.y):
				pixel = img.getpixel((i, j))

				if pixel == (0, 0, 0):
					dw_scale_pos = V2(i, j) / self.downscale
					block = Block(dw_scale_pos)
					self.map_objects.append(block)

	def __init__(self, path, block_size, downscale=V2(1, 1)):
		self.path = path
		self.block_size = block_size
		self.downscale = downscale

		self.size = None
		self.map_objects = []

		self.load_map()
