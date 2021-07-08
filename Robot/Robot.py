from common.position import Position
from Sensors import RF_Sensor
import threading
from time import sleep
from math import *
class Robot:
	class RobotPosition(Position):
		__slot__ = ["_x", "_y", "_z", "_roll", "_pitch", "_yaw"]
		def __init__(self,  x,y,z, roll = 0, pitch = 0, yaw = 0):
			super().__init__(x,y,z)
			self._roll = roll
			self._pitch = pitch
			self._yaw = yaw
		def get(self):
			return (self._x, self._y, self._z, self._roll, self._pitch, self._yaw)
		def set(self, x,y,z,r,p,yaw):
			self._x = x
			self._y = y
			self._z = z
			self._roll = r
			self._pitch = p
			self._yaw = yaw
		def update(self, v, w, dt):
			self._x += v*cos(self._yaw)*dt
			self._y += v*sin(self._yaw)*dt
			self._yaw += w*dt



	def __init__(self, x = 0,y = 0,z = 0, roll = 0, pitch = 0, yaw = 0):
		self._position = self.RobotPosition(x,y,z,roll,pitch,yaw)
		self._Sensors = []




class Combo(Robot):
	def __init__(self, x = 0, y = 0, z = 0, roll = 0, pitch = 0, yaw = 0):
		super().__init__()
		self._S1 = RF_Sensor(self._position, 0.2, -0.2, 0)
		self._S2 = RF_Sensor(self._position, 0.2, 0.2, 0)
		self._S3 = RF_Sensor(self._position, -0.1, 0, 0.3)
		self.Sensors = [self._S1, self._S2, self._S3]
		self._tag_position = Position(0,0,0)
		self._hz = 60

		self._data = [0, 0, 0]
		self._SensorThread = threading.Thread(target = self._get_sensors)
		self._SensorThread.daemon = True
		self._SensorThread.start()

	def _get_sensors(self):
		while True:
			for i in range(3):
				self._data[i] = self.Sensors[i].get(self._tag_position)
			sleep(1/self._hz)
	def set_tag_position(self, P):
		self._tag_position = P

	def follow(self):
		x,y,z,r,p,yaw = self._position.get()
		tx,ty,tz=self._tag_position.get()
		k1 = 1
		k2 = 3
		e1 = cos(yaw)*(tx - x) + sin(yaw)*(ty - y)
		e2 = -sin(yaw)*(tx - x) + cos(yaw)*(ty - y)
		v = k1*e1
		w = k2*e2
		#print(v,w)
		self._position.update(v,w,1/self._hz)
	def recognition(self):
		pass
	def get_position(self):
		return self._position.get()
	def _sync(self):

		for sensor in self.Sensors:
			sensor.update_position()

	def run(self):
		while True:
			self.recognition()
			self.follow()
			self._sync()
			sleep(1/self._hz)


if __name__=="__main__":
	test = Combo()
	test.run()

