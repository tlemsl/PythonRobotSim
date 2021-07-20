import pandas as pd
import numpy as np
import time
import threading
import matplotlib.pyplot as plt
class Logger:
	def __init__(self, name, variable, hz,columns=None, plot_flag = True):
		self._name = name
		self._hz = hz
		self.flag = True
		self._columns = columns
		self._plot_flag = plot_flag
		self._target = variable
		self._data = []

		self._init_time = time.time()
		self._Logging_thread = threading.Thread(target = self._logging)
		self._Logging_thread.daemon = True
		self._Logging_thread.start()
		print(f"Start Logging {self._name}")
	def _logging(self):
		while True:
			if self.flag:
				data = [time.time() - self._init_time]
				if type(self._target) == "class":
					try:
						for d in self._target.get(): data.append(d)
					except:
						print("can't logging variable")
						self.__del__()
				else:
					for d in self._target: data.append(d)
				self._data.append(data)
			time.sleep(1/self._hz)
		self.__del__()

	def get(self):
		return self._data

	def __del__(self):
		self.save()
		if self._plot_flag:
			self._plot()

	def save(self):
		if self._columns == None:
			self._columns = [f"Variable {i}" for i in range(len(self._data[0]))]
			self._columns[0] = "Time(s)"
		else:
			self._columns.insert(0, "Time(s)")

		save_data = pd.DataFrame(self._data, columns=self._columns)
		save_data = save_data.set_index("Time(s)")
		save_data.to_csv(f"~/Desktop/{self._name}.csv")
		print(f"{self._name} Data save! length : {len(self._data)}")
		print(save_data)

	def _plot(self):
		if self._plot_flag:
			data = np.array(self._data)
			fig, axes = plt.subplots(1, len(self._columns)-1, sharex=True)
			for i in range(len(self._columns) - 1):
				axes[i].plot(data[:,0], data[:,i+1])
				min = data[:, i+1].min()
				max = data[:, i+1].max()
				axes[i].set_title(self._columns[i+1])
				axes[i].set_xlabel("Time(s)")
				axes[i].set_ylabel(self._columns[i+1])
				axes[i].set_ylim([min, max])
			fig.suptitle(self._name)
			plt.show()
	def stop(self):
		self.__del__()



if __name__=="__main__":
	a = [1,1,2]
	log = Logger("test", a, 1)
	for i in range(5):
		a[0] = i
		a[1] = i + 10
		a[2] = i + 100
		time.sleep(1)
