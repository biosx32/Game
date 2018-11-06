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


class Action:
	def __init__(self, type, data=None):
		self.type = type
		self.data = data

	def unpack(self):
		return self.type, self.data


class GameObject:
	_sharedID_counter = 0

	def is_active(self):
		return len(self._actions) > 0

	def add_action(self, action: Action):
		self._actions.append(action)

	def get_actions(self):
		return self._actions[:]

	def update_actions(self, actions):
		self._actions = actions

	def __init__(self, pos, tname=None):
		if not isinstance(pos, (V2,)):
			pos = V2(0, 0)

		self.pos = pos.copy()
		self.tname = tname
		self.rID = None
		self.gID = GameObject._sharedID_counter
		GameObject._sharedID_counter += 1

		self._collisionCheck = False
		self.in_collision = False
		self._actions = []

	def set_rID(self, number):
		self.rID = number

	def __str__(self):
		return "{}:{} at {}".format(self.tname, self.rID, self.pos)

	def __repr__(self):
		return str(self)


class Block(GameObject):
	def __init__(self, pos):
		super().__init__(pos, tname='block')


class Player(GameObject):
	def __init__(self, pos):
		super().__init__(pos, tname='player')
		self.type = 'player'
		self.gaccel = 0.0
		self.jmp_energy = 0.0


class Camera(GameObject):
	def __init__(self, pos=None):
		pos = pos or V2(0, 0)
		super().__init__(pos, tname='camera')
		self.type = 'player'


class GameMap:

	def getobject(self, ID, relative_to=None) -> GameObject:
		if relative_to is not None:
			group_dict = self.object_dict[relative_to]
			if ID in group_dict.keys():
				return group_dict[ID]

		else:
			gmo: GameObject
			for gmo in self.map_objects:
				if gmo.gID == ID:
					return gmo

		return None


	def delobject(self, ID, by_group=None):
		obj = self.getobject(ID, by_group)
		if not obj:
			print("Cannot delete object:", ID)
			return

		self.require_vo_update()
		self.map_objects.remove(obj)
		del self.object_dict[obj.tname][obj.rID]


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

		gmo.set_rID(key)

		self.map_objects.append(gmo)
		self.object_dict[gmo.tname][key] = gmo

	def update_vo_list_from(self, new_list: list):
		self.visible_objects = new_list
		self.vo_update_required = False

	def require_vo_update(self):
		self.vo_update_required = True

	def get_vo_list(self) -> list:
		return self.visible_objects[:]

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
		self.b_size_xy = block_size
		self.downscale = downscale
		self.size = None

		self._id_counter = {}
		self.object_dict = {}
		self.map_objects = []
		self.visible_objects = []

		self.vo_update_required = True

		self.load_map()
