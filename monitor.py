import psutil

def get_cpu():
    return psutil.cpu_percent(interval=1)

def get_ram():
    return psutil.virtual_memory().percent

def get_disk(path="C:\\"):
    disk = psutil.disk_usage(path)
    return disk.percent

def get_system_info():
    return {
        "cpu": get_cpu(),
        "ram": get_ram(),
        "disk": get_disk()
    }

def main():
    info = get_system_info()

    print(f"CPU: {info['cpu']:.1f}%")
    print(f"RAM: {info['ram']:.1f}%")
    print(f"DISK: {info['disk']:.1f}%")

if __name__ == "__main__":
    main()
