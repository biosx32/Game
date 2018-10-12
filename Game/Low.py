import sys


class V2:
	def __init__(self, x=(0, 0), y=None):
		if y is None:
			x, y = x

		self.x, self.y = x, y
		self._data = x, y

	def __eq__(self, other):
		return not self.NEQ(other)

	def NEQ(self, other, tolerance=0.001):
		return abs(self.x - other.x) + abs(self.y - other.y) > tolerance

	def __neg__(self):
		return V2(-self.x, -self.y)

	def __sub__(self, other):
		return V2(self.x - other.x, self.y - other.y)

	def __add__(self, other):
		return V2(self.x + other.x, self.y + other.y)

	def __truediv__(self, other):
		if isinstance(other, (int, float)):
			other = V2(other, other)
		return V2(self.x / other.x, self.y / other.y)

	def __rmul__(self, other):
		return self * other

	def __mul__(self, other):
		if isinstance(other, (int, float)):
			other = V2(other, other)

		return V2(self.x * other.x, self.y * other.y)

	def __iter__(self):
		self.n = -1
		return self

	def __next__(self):
		self.n += 1
		if self.n == len(self._data):
			raise StopIteration("Too many values required")

		return self._data[self.n]

	def __str__(self):
		return "({:.2f}, {:.2f})".format(self.x, self.y)

	def rectify(self):
		return V2(self.x if self.x > 0 else 0,
				self.y if self.y > 0 else 0)

	def restrict(self, other):
		return V2(self.x if self.x <= other.x-1 else other.x - 1,
				self.y if self.y <= other.y-1 else other.y - 1)

	def to_integer(self):
		return V2(int(self.x), int(self.y))

	def to_tuple(self):
		return self.x, self.y

	def multiply_i(self, other):
		return (self.pos * other.pos).to_intger()


def assert_error(condition, msg: str):
	if not condition:
		print("Error:", msg)
		print("-------- pausing ---------")
		input()
		sys.exit(-1)