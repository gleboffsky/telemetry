from datetime import datetime, date, time
import platform
import psutil
import subprocess, re
import os


class SystemInfo():

	''' 
		Класс SystemInfo собирает данные о системе на которой запущен скрипт.
		
		Вызов метода get_system_info вернет данные в виде JSON, которые включают в себя:
			date и time => дату и время окончания сбора данных
			systeminfo => словарь содержащий более подробную информацию о компьютере
				architecture => архитектура компьютера
				cpu { => словарь содержащий информацию о процессоре
						name => название процессора,
						frequency => частота процессора,
						temperature => температура процессора
				}
				battery => процент заряда батареи
	'''

	def __init__(self): pass

	def _get_architecture(self):
		return platform.architecture()

	def _get_percent_battery(self):
		return psutil.sensors_battery().percent

	def _get_cpu_frequency(self):
		return psutil.cpu_freq().current # current frequencies expressed in Mhz

	def _get_cpu_name(self):
		if platform.system() == "Windows":
			return platform.processor()
		elif platform.system() == "Linux":
			command = "cat /proc/cpuinfo"
			all_info = subprocess.check_output(command, shell=True).strip()
			for line in all_info.split('\n'):
				if "model_name" in line:
					return re.sub(".*model name*.:", "", line, 1)

	def _get_temperature_cpu(self):
		if platform.system() == "Windows":
			import wmi
			w = wmi.WMI(namespace="root\\wmi")
			for elem in w.MSAcpi_ThermalZoneTemperature():
				return elem.CurrentTemperature # kelvins
		elif platform.system() == "Linux":
			return psutil.sensors_temperatures()

	def _get_date_now(self):
		return datetime.now().strftime("%d-%m-%Y")
	def _get_time_now(self):
		return datetime.now().strftime("%H:%M")

	def get_system_info(self):
		return {
			"date": self._get_date_now(),
			"time": self._get_time_now(),
			"systeminfo": {
				"architecture": self._get_architecture(),
				"cpu": {
					"name": self._get_cpu_name(),
					"frequency": self._get_cpu_frequency(),
					"temperature": self._get_temperature_cpu()
				},
				"battery": self._get_percent_battery()
			}
		}



if __name__ == "__main__":
	print(SystemInfo.get_system_info())
