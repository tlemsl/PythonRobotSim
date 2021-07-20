from math import *
import time


class PID:
	def __init__(self, KP, KI, KD, AW):
		self._kp = KP
		self._ki = KI
		self._kd = KD
		self._aw = AW
		self._errors=[0,0,0]
		self._error=0
		self._prev_error = 0
		self._prev_time = time.time()
	def set_target(self):
		pass
	def set_present(self):
		pass
	def set_error(self, error):
		self._error = error

	def get(self, error):
		dt = time.time() - self._prev_time
		dt = 1/60
		self._prev_time = time.time()
		self._error = error
		self._errors[0] = self._error
		self._errors[1] += self._error*dt
		self._errors[1] = min(self._aw, max(-self._aw, self._errors[1]))
		self._errors[2] = (self._error - self._prev_error)/dt
		self._prev_error = self._error
		print( self._errors)
		return self._kp*self._errors[0]+self._ki*self._errors[1]+self._kd*self._errors[2]

