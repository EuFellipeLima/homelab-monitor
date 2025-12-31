import psutil
import platform
import time

def get_cpu():
    return psutil.cpu_percent(interval=1)

def get_ram():
    return psutil.virtual_memory().percent

def get_disk():
    system = platform.system()

    if system == "Windows":
        path = "C:\\"
    elif system == "Linux":
        path = "/"
    elif system == "Darwin":
        path = "/"
    else:
        raise RuntimeError(f"Unsupported operating system: {system}")

    disk = psutil.disk_usage(path)
    return disk.percent

def get_system_uptime():
    boot_time = psutil.boot_time()
    now = time.time()
    uptime_seconds = int(now - boot_time)
    return uptime_seconds

def format_seconds(seconds):
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60

    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    elif minutes > 0:
        return f"{minutes}m"
    else:
        return "less than 1m"


def get_system_info():
    return {
        "cpu": get_cpu(),
        "ram": get_ram(),
        "disk": get_disk(),
        'uptime': get_system_uptime()
    }

def main():
    info = get_system_info()

    print(f"CPU: {info['cpu']:.1f}%")
    print(f"RAM: {info['ram']:.1f}%")
    print(f"DISK: {info['disk']:.1f}%")
    print(f"UPTIME: {format_seconds(info['uptime'])}")

if __name__ == "__main__":
    main()
