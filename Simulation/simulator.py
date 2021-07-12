import os
import sys
import matplotlib.pyplot as plt
import time
import threading
import cv2
import numpy as np
import time
dir = os.getcwd()
sys.path.append(dir+"/../Robot")
from common.logger import Logger

class Simulator:
	def __init__(self):
		self._resolution = 100
		self._size = 500
		self.set_robot()
		self._hz = 60.0

		self._main_img = np.zeros((self._size,self._size,3), np.uint8)

		#self._RobotPositionLogger = Logger("Robot Position", self.Robot, self._hz)
		cv2.namedWindow('Simulation')
		cv2.setMouseCallback('Simulation',self.set_point)
		self._init_time = time.time()
		self._RobotThread = threading.Thread(target = self.Robot.run )
		self._RobotThread.daemon = True
		self._RobotThread.start()
		"""self._PlotThread = threading.Thread(target = self.plotting)
								self._PlotThread.daemon = True
								self._PlotThread.start()"""

	def _get_sim_time(self):
		return time.time() - self._init_time
	def plotting(self):
		pass
	def drawing(self):
		pass

	def set_robot(self):
		self.Robot = None

	def set_point(self, event, x, y, flags, param):
		if event == cv2.EVENT_LBUTTONUP:
			cv2.circle(self._main_img,(x,y),10,(255,0,0),-1)

	def run(self):
		while True:
			self.drawing()
			cv2.imshow("Simulation", self._main_img)
			key = cv2.waitKey(int(1000/self._hz))
			self._main_img = np.zeros((self._size,self._size,3), np.uint8)
			if key & 0xFF == 27:
				cv2.destroyAllWindows()
				break
		self.__del__()
	def __del__(self):

		self.Robot.stop()		
		print("Stop Simulation")


