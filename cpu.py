import psutil
import os

#1. Получите информацию о процессоре

# cpuCount = psutil.cpu_count()  # логический номер процессора
# print('Logical processor number: ', cpuCount)
# cpulogical = psutil.cpu_count(logical=False)  # физическое ядро
# print('CPU Physical core:', cpulogical)
#
# # 2. Статистика пользователя ЦП / системы / простоя:
#
# cpuTimes = psutil.cpu_times()
# print('Пользователь ЦП / система / время простоя:', cpuTimes)
#
# # 3. Информация о памяти
#
# cpuMemory = psutil.virtual_memory()
# cpuSwap = psutil.swap_memory()
#
# print('cpuMemory:', cpuMemory)
# print('информация об области обмена ЦП:', cpuSwap)
#
# # 4. Получить информацию о диске
#
# cpuPart = psutil.disk_partitions()  # Информация о разделе диска
# cpuUsage = psutil.disk_usage('/')  # Использование диска
# cpuCounters = psutil.disk_io_counters()  # ввод-вывод диска
# print('использование диска cpu:', cpuUsage)
# print('диск IO:', cpuCounters)
#
# # 5. Получите информацию о сети.
#
# netCounters = psutil.net_io_counters()  # Получить количество байтов / пакетов чтения и записи по сети
# print('Количество байтов / пакетов чтения и записи в сети:', netCounters)
#
#
#
# # 6. Текущуя информация о сетевом подключении:
#
#
#
# # 7. Информация о процессах
#
# #
# netPids = psutil.pids()
# netProcess = psutil.Process(netPids[1])
#
# netFa = netProcess.ppid()  # ID родительского процесса
# print('ID родительского процесса:', netFa)
# netparent = netProcess.parent()  # родительский процесс
# print('родительский процесс:', netparent)
#
#
#
#
# # netName = netProcess.username()  # Process username
# # print('Имя пользователя:', netName)
# netcreateTime = netProcess.create_time()  # Время создания процесса
# print('Время создания процесса:', netcreateTime)
# print(netProcess.create_time())
# # print(type(str(netcreateTime)))
#
# nettimes = netProcess.cpu_times()  # Процессорное время, используемое процессом
# print('Процессорное время, используемое процессом:', nettimes)
# netMemoryInfo = netProcess.memory_info()  # Память, используемая процессом
# print('Память, используемая процессом:', netMemoryInfo)
# netthreads = netProcess.num_threads()  # Количество потоков процесса
# print('Количество потоков в процессе:', netthreads)
temperature = psutil.sensors_temperatures()  # Temperature sensors



# data = []
# for x in psutil.sensors_temperatures():
#     data.append({
#         "device": x.device,
#         "mountpoint": x.mountpoint,
#         "fstype": x.fstype,
#         "opts": x.opts
#     })
# for x in psutil.disk_partitions():
#     query1 = "INSERT INTO test (device,mountpoint,fstype) VALUES(%s,%s,%s)"
#     cursor.executemany(query1, [str("x","y","z")])

