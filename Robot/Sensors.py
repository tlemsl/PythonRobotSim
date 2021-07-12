from common.position import Position
import numpy as np
from math import *
class Sensor:
	class SensorPosition(Position):
		def __init__(self, P, x,y,z):
			self._robot_position = P
			self._relative_position = Position(x,y,z)
			yaw = self._robot_position._yaw
			self._x = self._robot_position._x + (cos(yaw)*x - sin(yaw)*y)
			self._y = self._robot_position._y + (sin(yaw)*x + cos(yaw)*y)
			self._z = z
		def update(self):
			yaw = self._robot_position._yaw
			self._x = self._robot_position._x + (cos(yaw)*self._relative_position._x - sin(yaw)*self._relative_position._y)
			self._y = self._robot_position._y + (sin(yaw)*self._relative_position._x + cos(yaw)*self._relative_position._y)

			
	def __init__(self, P, x=0, y=0, z=0, std = 0.1):
		self._std = std
		self._position = self.SensorPosition(P,x,y,z)

	def set_position(self, x,y,z):
		self._position.set(x,y,z)
	def update_position(self):
		self._position.update()
	def __del__(self):
		pass
	def stop(self):
		self.__del__()



class RF_Sensor(Sensor):
	
	def get(self, P):
		distance = self._position.get_distance(P)
		return np.random.normal(distance, self._std, size=1)[0]
	def get_position(self):
		return self._position.get()