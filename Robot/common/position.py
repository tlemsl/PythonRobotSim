import math
class Position:
	__slot__ = ["_x", "_y", "_z"]
	def __init__(self,x,y,z):
		self._x = x
		self._y = y
		self._z = z

	def get_distance(self, o):
		return math.sqrt( (o._x - self._x)**2 + (o._y - self._y)**2 + (o._z - self._z)**2 )


	def set(self ,x, y, z):
		self._x = x
		self._y = y
		self._z = z

	def get(self):
		return (self._x, self._y, self._z)
	def __add__(self, other):
		return self._x + other._x, self._y + other._y, self._z + other._z
	def __sub__(self, other):
		return self._x - other._x, self._y - other._y, self._z - other._z