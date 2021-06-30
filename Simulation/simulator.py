import os
import sys
import matplotlib.pyplot as plt
import time
import threading
import cv2
import numpy as np
dir = os.getcwd()
sys.path.append(dir+"/../Robot")


class Simulator:
	def __init__(self):
		self._resolution = 100
		self.set_robot()
		self._hz = 10.0

		self._main_img = np.zeros((500,500,3), np.uint8)


		cv2.namedWindow('Simulation')
		cv2.setMouseCallback('Simulation',self.set_point)

		self._RobotThread = threading.Thread(target = self.Robot.run )
		self._RobotThread.daemon = True
		self._RobotThread.start()
		"""self._MainThread = threading.Thread(target = self.run )
								self._MainThread.daemon = True
								self._MainThread.start()
								"""

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
			self._main_img = np.zeros((500,500,3), np.uint8)
			if key & 0xFF == 27:
				cv2.destroyAllWindows()
				break



