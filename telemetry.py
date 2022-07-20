from mysql.connector import errorcode
from sys import platform
import mysql.connector
import config
import http.client
import psutil
global cnx, cnx2

# System info
cpuPhysical = psutil.cpu_count(logical=False)  # CPU Physical core
cpuLogical = psutil.cpu_count()  # Logical processor number
cpuTimes = psutil.cpu_times()  # CPU User Statistics
cpuMemory = psutil.virtual_memory()  # Memory information
cpuSwap = psutil.swap_memory()  # CPU swap area information
cpuPart = psutil.disk_partitions()  # Disk partition information
cpuUsage = psutil.disk_usage('/')  # Disk Usage
cpuCounters = psutil.disk_io_counters()  # disk I / O
netCounters = psutil.net_io_counters()  # Number of bytes / packets read and write over the network
netAddress = psutil.net_if_addrs()  # Information about a network interface
netStatus = psutil.net_if_stats()  # Network interface status
netConnection = psutil.net_connections()  # Information about the current network connection
netPids = psutil.pids()
netProcess = psutil.Process(netPids[1])
netFa = netProcess.ppid()  # Parent process ID
netParent = netProcess.parent()  # Parent process
netParentChildren = netProcess.children()  # List of child processes
procStatus = netProcess.status()  # Process status
netUserName = netProcess.username()  # Process username
netCreateTime = netProcess.create_time()  # Process creation time
netThreads = netProcess.num_threads()  # Number of process threads
conn = http.client.HTTPConnection("ifconfig.me")
conn.request("GET", "/ip")
a = conn.getresponse().read()
b = str(a)
ip = b.replace("b", "")


if platform == "linux" or platform == "linux2":
    try:
        cnx = mysql.connector.connect(**config.login)
        cursor = cnx.cursor()

        # data = []
        # for x in psutil.disk_partitions():
        #     data.append({
        #         "device": x.device,
        #         "mountpoint": x.mountpoint,
        #         "fstype": x.fstype,
        #         "opts": x.opts
        #     })
        # for x in psutil.disk_partitions():
        #     query1 = "INSERT INTO test (device,mountpoint,fstype) VALUES(%s,%s,%s)"
        #     cursor.executemany(query1, [str("x","y","z")])

        cursor.execute("CREATE TABLE IF NOT EXISTS host (idh varchar(10), id int AUTO_INCREMENT primary key, host varchar(20), unique key(host) )")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS DynamicMetrics (id int AUTO_INCREMENT primary key,idh varchar(10) unique, "
            "time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, "
            "user varchar(20), nice varchar(20), system varchar(20), idle varchar(20), iowait varchar(20), "
            "irq varchar(20), softirq varchar(20), steal varchar(20), quest varchar(20), quest_nice varchar(20), "
            "total varchar(20), available varchar(20), percent varchar(20), used varchar(20), free varchar(20), "
            "active varchar(20), inactive varchar(20), buffers varchar(20), cached varchar(20),shared varchar(20), "
            "slab varchar(20),totalswap varchar(20), usedswap varchar(20), freeswap varchar(20), percentswap varchar("
            "20), sinswap varchar(20), soutswap varchar(20), totaldisk varchar(20), useddisk varchar(20), "
            "freedisk varchar(20), percentdisk varchar(20),timecreate varchar(20), threads varchar(20), temperature "
            "varchar(40))")

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS StaticMetrics (id int AUTO_INCREMENT primary key,idh varchar(10) unique, logiccores "
            "int, physicalcores int, ram varchar(15), diskmemory varchar(15))")
        cursor.execute("ALTER TABLE host ADD FOREIGN KEY (idh) REFERENCES DynamicMetrics(idh)")
        cursor.execute("ALTER TABLE host ADD FOREIGN KEY (idh) REFERENCES StaticMetrics(idh)")

        query1 = "INSERT IGNORE INTO host (host) VALUES (%s)"
        cursor.execute(query1, [ip])
        # query2 = "idh"
        # cursor.execute(query2,[ip])
        query3 = "INSERT INTO StaticMetrics (logiccores) VALUES (%s)"
        cursor.execute(query3, [cpuLogical])
        query4 = "INSERT INTO StaticMetrics (physicalcores) VALUES (%s)"
        cursor.execute(query4, [cpuPhysical])
        query5 = "INSERT INTO StaticMetrics (ram) VALUES (%s) "
        cursor.execute(query5, [cpuMemory[0]])
        query6 = "INSERT INTO StaticMetrics (diskmemory) VALUES (%s) "
        cursor.execute(query6, [cpuUsage[0]])
        query7 = "INSERT INTO DynamicMetrics (user,nice,system,idle,iowait,irq,softirq,steal,quest,quest_nice) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.executemany(query7, [cpuTimes])
        query8 = "INSERT INTO DynamicMetrics (total,available,percent,used,free,active,inactive,buffers,cached,shared,slab) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.executemany(query8, [cpuMemory])
        query9 = "INSERT INTO DynamicMetrics (totalswap, usedswap, freeswap, percentswap,sinswap,soutswap) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.executemany(query9, [cpuSwap])
        query10 = "INSERT INTO DynamicMetrics (totaldisk,useddisk,freedisk,percentdisk) VALUES (%s,%s,%s,%s) "
        cursor.executemany(query10, [cpuUsage])
        query11 = "INSERT INTO DynamicMetrics (timecreate) VALUES (%s) "
        cursor.execute(query11, [netCreateTime])
        query12 = "INSERT INTO DynamicMetrics (threads) VALUES (%s)"
        cursor.execute(query12, [netThreads])
        temperature = psutil.sensors_temperatures()  # Temperature sensors
        temp_core = 0
        for core in temperature['coretemp']:
            temp_core += core.current
        temp = (temp_core / 3)
        query13 = "INSERT INTO DynamicMetrics (temperature) VALUES (%s)"
        cursor.execute(query13, [temp])

        cnx.commit()
        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


elif platform == "win32":
    try:
        cnx2 = mysql.connector.connect(**config.login2)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    cursor2 = cnx2.cursor()
    import wmi
    computer = wmi.WMI()
    computer_info = computer.Win32_ComputerSystem()[0]
    os_info = computer.Win32_OperatingSystem()[0]
    proc_info = computer.Win32_Processor()[0]
    gpu_info = computer.Win32_VideoController()[0]
    os_name = os_info.Name.encode('utf-8').split(b'|')[0]
    os_version = ' '.join([os_info.Version, os_info.BuildNumber])
    system_ram = float(os_info.TotalVisibleMemorySize) / 1048576  # KB to GB

    cursor2.execute(
        "CREATE TABLE IF NOT EXISTS host (idh varchar(10), id int AUTO_INCREMENT primary key, host varchar(20), unique key(host))")
    cursor2.execute(
        "CREATE TABLE IF NOT EXISTS DynamicMetrics (id int AUTO_INCREMENT primary key,idh varchar(10) unique, "
        "time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, "
        "user varchar(20), system varchar(20), idle varchar(20),interrupt varchar(20),dpc varchar(20),"
        "total varchar(20), available varchar(20), percent varchar(20), used varchar(20), free varchar(20),"
        "totalswap varchar(20), usedswap varchar(20), freeswap varchar(20), percentswap varchar("
        "20), sinswap varchar(20), soutswap varchar(20), totaldisk varchar(20), useddisk varchar(20), "
        "freedisk varchar(20), percentdisk varchar(20),timecreate varchar(20), threads varchar(20), temperature "
        "varchar(40))")
    cursor2.execute(
        "CREATE TABLE IF NOT EXISTS StaticMetrics (id int AUTO_INCREMENT primary key,idh varchar(10) unique, logiccores "
        "int, physicalcores int, ram varchar(35), diskmemory varchar(15),os varchar(30),cpu varchar(50),gpu varchar(50))")
    cursor2.execute("ALTER TABLE host ADD FOREIGN KEY (idh) REFERENCES DynamicMetrics(idh)")
    cursor2.execute("ALTER TABLE host ADD FOREIGN KEY (idh) REFERENCES StaticMetrics(idh)")
    query11 = "INSERT IGNORE INTO host (host) VALUES (%s)"
    cursor2.execute(query11,[ip])
    # query22 = "idh"
    # cursor2.execute(query22,[ip])
    query33 = "INSERT INTO StaticMetrics (logiccores) VALUES (%s)"
    cursor2.execute(query33, [cpuLogical])
    query44 = "INSERT INTO StaticMetrics (physicalcores) VALUES (%s)"
    cursor2.execute(query44, [cpuPhysical])
    query55 = "INSERT INTO StaticMetrics (ram) VALUES (%s) "
    cursor2.execute(query55, [system_ram])
    query66 = "INSERT INTO StaticMetrics (diskmemory) VALUES (%s) "
    cursor2.execute(query66, [cpuUsage[0]])
    query77 = "INSERT INTO StaticMetrics (os) VALUES (%s) "
    cursor2.execute(query77, [os_version])
    query88 = "INSERT INTO StaticMetrics (cpu) VALUES (%s) "
    cursor2.execute(query88, [proc_info.Name])
    query99 = "INSERT INTO StaticMetrics (gpu) VALUES (%s) "
    cursor2.execute(query99, [gpu_info.Name])
    query100 = "INSERT INTO DynamicMetrics (user,system,idle,interrupt,dpc) VALUES (%s,%s,%s,%s,%s)"
    cursor2.executemany(query100, [cpuTimes])
    query111 = "INSERT INTO DynamicMetrics (total,available,percent,used,free) VALUES (%s,%s,%s,%s,%s)"
    cursor2.executemany(query111, [cpuMemory])
    query120 = "INSERT INTO DynamicMetrics (totalswap, usedswap, freeswap, percentswap,sinswap,soutswap) VALUES (%s,%s,%s,%s,%s,%s)"
    cursor2.executemany(query120, [cpuSwap])
    query130 = "INSERT INTO DynamicMetrics (totaldisk,useddisk,freedisk,percentdisk) VALUES (%s,%s,%s,%s) "
    cursor2.executemany(query130, [cpuUsage])
    query140 = "INSERT INTO DynamicMetrics (timecreate) VALUES (%s) "
    cursor2.execute(query140, [netCreateTime])
    query150 = "INSERT INTO DynamicMetrics (threads) VALUES (%s)"
    cursor2.execute(query150, [netThreads])


    cnx2.commit()
    cursor2.close()
    cnx2.close()
