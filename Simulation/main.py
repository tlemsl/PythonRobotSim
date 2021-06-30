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

class ComboSim(Simulator):
	def __init__(self):
		self._tag_position = Position(0,0,0)

		super().__init__()

	def set_robot(self):
		self.Robot = Combo()

	def set_point(self, event, x, y, flags, param):

		if event == cv2.EVENT_LBUTTONUP:
			self._tag_position.set((x-250)/self._resolution,-(y-250)/self._resolution,0)
			self.Robot.set_tag_position(self._tag_position)

	def drawing(self):
		x,y,_,_,_,_ = self.Robot.get_position()
		#print(x,y)
		cv2.circle(self._main_img,(int(x*self._resolution+250),int(250 - y*self._resolution)),3,(255,255,255),-1)
		for Sensor in self.Robot.Sensors:
			x,y,z = Sensor.get_position()
			print(x,y,z)
			cv2.circle(self._main_img,(int(x*self._resolution+250),int(250 - y*self._resolution)),1,(0,255,255),-1)

		x,y,_ = self._tag_position.get()
		cv2.circle(self._main_img,(int(x*self._resolution+250),int(250 - y*self._resolution)),1,(255,0,0),-1)


if __name__ == "__main__":
	Simulation = ComboSim()
	Simulation.run()
