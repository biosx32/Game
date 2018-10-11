
class V2():
	def __init__(self, x, y):
		self.x, self.y = x, y
		self._data = (x, y)

	def __eq__(self, other):
		return not self.NEQ(other)

	def NEQ(self, other, tolerance=0.001):
		return abs(self.x - other.x) + abs(self.y - other.y) > tolerance

	def __neg__(self):
		return V2(-self.x, -self.y)

	def __sub__(self, other):
		return V2(self.x - other.x, self.y - other.y)

	def __add__(self, other):
		return V2(self.x +other.x, self.y + other.y)

	def __truediv__(self, o):
		return V2(self.x/o, self.y/o)

	def __mul__(self, other):
		if type(other) == int:
			return V2(self.x*other, self.y*other)
		if type(other) == V2:
			return V2(self.x * other.x, self.y * other.y)
		raise NotImplementedError

	def __iter__(self):
		self.n = -1
		return self

	def __next__(self):
		self.n += 1
		if self.n == len(self._data):
			raise StopIteration("Too many values required")

		return self._data[self.n]

	def __str__(self):
		return str((self.x, self.y))

	def ToAboveZero(self):
		return V2(self.x if self.x > 0 else 0,
				self.y if self.y > 0 else 0)

	def ToMaximum(self, other):
		return V2(self.x if self.x <= other.x-1 else other.x - 1,
				self.y if self.y <= other.y-1 else other.y - 1)

	def ToIntegerTup(self):
		return V2(int(self.x), int(self.y))

class Animation():
	# --- just an idea ...
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



class GameObject():
	def __init__(self):
		self._collisionCheck = False

class Block(GameObject):
	def __init__(self, pos):
		self.pos = pos

		self.type = 'basic'

	def drawable(self):
		return True

	def __str__(self):
		return "{}: ({}) [{}]".format(self.name, self.pos, self.size)




class CollisionObject(Basic):
	def __init__(self):
		self._collisionCheck = True

class Player(Basic):
	def __init__(self, pos=V2(2, 2), name='player-1'):
		self.type = 'player'
		self.pos = pos
		self.name = name
		self.size = V2(50,51)