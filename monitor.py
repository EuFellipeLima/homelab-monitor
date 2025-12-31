import psutil
import platform
import time

try:
    import distro
except ImportError:
    distro = None

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
    
def get_os_info():
    system = platform.system()
    kernel = None

    if system == "Windows":
        ver, build, sp, _ = platform.win32_ver()
        os_name = f"Windows {ver} {sp} (Build: {build})".strip()
    elif system == "Darwin":
        ver, _, _ = platform.mac_ver()
        kernel = platform.release()
        os_name = f"macOS {ver} ({kernel})"
    elif system == "Linux":
        kernel_ver = platform.release()
        kernel = f"Linux {kernel_ver}"
        os_name = f"{distro.name(pretty=True)}" if distro else system
    else:
        os_name = system

    return os_name, kernel


def get_system_info():
    os_name, kernel = get_os_info()
    return {
        "cpu": get_cpu(),
        "ram": get_ram(),
        "disk": get_disk(),
        'uptime': get_system_uptime(),
        'hostname': platform.node(),
        'os': os_name,
        'kernel': kernel
    }

def main():
    info = get_system_info()

    print(f"HOSTNAME: {info['hostname']}")
    print(f"OS: {info['os']}")
    if info['kernel']:
        print(f"KERNEL: {info['kernel']}")
    print(f"CPU: {info['cpu']:.1f}%")
    print(f"RAM: {info['ram']:.1f}%")
    print(f"DISK: {info['disk']:.1f}%")
    print(f"UPTIME: {format_seconds(info['uptime'])}")

if __name__ == "__main__":
    main()
