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
	_sharedID_counter = 0
	def __init__(self, pos, tname=None):
		if not pos:
			pos = V2(0, 0)

		self.pos = pos
		self.tname = tname
		self.ID = -1

		self._collisionCheck = False
		self.shared_ID = self._sharedID_counter
		self._sharedID_counter += 1

	def SetID(self, number):
		self.ID = number

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
	_id_counter = {}
	object_dict = {}
	map_objects = []

	def getobject(self, ID, by_group=None) -> GameObject:
		if by_group:
			group_dict = self.object_dict[by_group]
			if ID in group_dict.keys():
				return group_dict[ID]

		else:
			for gmo in self.map_objects:
				if gmo.ID == ID:
					return gmo

		return None

	def _next_key(self, key_name) -> int:
		if not key_name in self._id_counter.keys():
			self._id_counter[key_name] = 0
		self._id_counter[key_name] += 1

		if not key_name in self.object_dict:
			self.object_dict[key_name] = {}

		return self._id_counter[key_name] - 1

	def add(self, gmo: GameObject):
		# if key for group doesn't exist
		key = self._next_key(gmo.tname)

		gmo.SetID(key)

		self.map_objects.append(gmo)
		self.object_dict[gmo.tname][key] = gmo

	def load_map(self):
		img = Image.open(self.path).convert(mode='RGB')
		self.size = (V2(img.size) / self.downscale).to_integer()

		for i in range(self.size.x):
			for j in range(self.size.y):
				pixel = img.getpixel((i, j))

				if pixel == (0, 0, 0):
					dw_scale_pos = V2(i, j) / self.downscale
					block = Block(dw_scale_pos)
					self.add(block)

	def __init__(self, path, block_size, downscale=V2(1, 1)):
		self.path = path
		self.block_size = block_size
		self.downscale = downscale
		self.size = None

		self.load_map()
