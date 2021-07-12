import os
import sys
from simulator import Simulator
import threading
import matplotlib.pyplot as plt
import time
import cv2
import numpy as np
dir = os.getcwd()
sys.path.append(dir+"/../Robot")

from Robot import Combo
from common.position import Position
from common.logger import Logger
class ComboSim(Simulator):
	def __init__(self):
		self._tag_position = Position(0,0,0)
		super().__init__()
	def set_robot(self):
		self.Robot = Combo()

	def set_point(self, event, x, y, flags, param):
		click = False
		if event == cv2.EVENT_LBUTTONDOWN:
			click = True

		if event == cv2.EVENT_MOUSEMOVE:
			self._tag_position.set((x-self._size/2)/self._resolution,-(y-self._size/2)/self._resolution,0)
			self.Robot.set_tag_position(self._tag_position)

	def drawing(self):
		x,y,_,_,_,_ = self.Robot.get_position()
		#print(x,y)
		cv2.circle(self._main_img,(int(x*self._resolution+self._size/2),int(self._size/2 - y*self._resolution)),3,(255,255,255),-1)
		for Sensor in self.Robot.Sensors:
			x,y,z = Sensor.get_position()
			cv2.circle(self._main_img,(int(x*self._resolution+self._size/2),int(self._size/2 - y*self._resolution)),2,(0,255,255),-1)

		x,y,_ = self._tag_position.get()
		cv2.circle(self._main_img,(int(x*self._resolution+self._size/2),int(self._size/2 - y*self._resolution)),5,(255,0,0),-1)

	def plotting(self):
		while True:
			x=self._get_sim_time()
			y = self.Robot._data[0]
			plt.scatter(x, y)
			plt.title("Real Time plot")
			plt.xlabel("x")
			plt.ylabel("sinx")
			time.sleep(1/self._hz)
		plt.show()


class ComboSimTest(ComboSim):
	def __init__(self, x,y,z):
		super().__init__()
		self._tag_position = Position(x,y,z)
		self.Robot.set_tag_position(self._tag_position)

	def set_point(self, event, x,y,flags,param):
		a=1
