import psutil
import platform
import time

try:
    import distro
except ImportError:
    distro = None

MACOS_VERSIONS = {
    "10.0": "Cheetah",
    "10.1": "Puma",
    "10.2": "Jaguar",
    "10.3": "Panther",
    "10.4": "Tiger",
    "10.5": "Leopard",
    "10.6": "Snow Leopard",
    "10.7": "Lion",
    "10.8": "Mountain Lion",
    "10.9": "Mavericks",
    "10.10": "Yosemite",
    "10.11": "El Capitan",
    "10.12": "Sierra",
    "10.13": "High Sierra",
    "10.14": "Mojave",
    "10.15": "Catalina",
    "11": "Big Sur",
    "12": "Monterey",
    "13": "Ventura",
    "14": "Sonoma",
    "15": "Sequoia",
    "26": "Tahoe"
}

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
        kernel_ver = platform.release()
        kernel = f"Darwin {kernel_ver}"
        major = int(ver.split(".")[0])

        if major >= 11:
            codename = MACOS_VERSIONS.get(str(major), "")
            os_name = f"macOS {codename} {ver}" if codename else f"macOS {ver}"
        else:
            ver_short = ".".join(ver.split(".")[:2])
            codename = MACOS_VERSIONS.get(ver_short, "")
            os_name = f"macOS {codename} {ver}" if codename else f"macOS {ver}"
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
