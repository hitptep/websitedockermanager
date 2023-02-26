import psutil

port = 8797

for proc in psutil.process_iter():
    try:
        for conn in proc.connections():
            if conn.laddr.port == port:
                print(f"Process {proc.pid} ({proc.name()}) is using port {port}")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
