import psutil
import platform
import time
import subprocess

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

IGNORE_FS = {
    "proc", "sysfs", "tmpfs", "devtmpfs",
    "overlay", "squashfs", "autofs"
}

def get_cpu():
    return psutil.cpu_percent(interval=1)

def get_ram_info():
    mem = psutil.virtual_memory()
    total_gb = bytes_to_gb(mem.total)
    used_gb = bytes_to_gb(mem.used)
    free_gb = bytes_to_gb(mem.available)

    return {
        "percent": mem.percent,
        "total_gb": total_gb,
        "used_gb": used_gb,
        "free_gb": free_gb
    }

def get_disks_info():
    disks = []

    for part in psutil.disk_partitions(all=False):
        if part.fstype.lower() in IGNORE_FS:
            continue

        try:
            usage = psutil.disk_usage(part.mountpoint)
        except PermissionError:
            continue

        disk = {
            "device": part.device,
            "mountpoint": part.mountpoint,
            "fstype": part.fstype,
            "percent": usage.percent,
            "used_gb": bytes_to_gb(usage.used),
            "total_gb": bytes_to_gb(usage.total),
        }

        disks.append(disk)

    return disks

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
    
def bytes_to_gb(bytes_value):
    return bytes_value / (1024 ** 3)
    
def get_os_info():
    system = platform.system()
    kernel = None

    if system == "Windows":
        ver, build, sp, _ = platform.win32_ver()
        os_name = f"Windows {ver} {sp} (Build: {build})".strip()
    elif system == "Darwin":
        real_ver = get_macos_version()
        kernel_ver = platform.release()
        kernel = f"Darwin {kernel_ver}"

        if real_ver:
            major = int(real_ver.split(".")[0])

        if major >= 11:
            codename = MACOS_VERSIONS.get(str(major), "")
            os_name = f"macOS {codename} {real_ver}" if codename else f"macOS {real_ver}"
        else:
            ver_short = ".".join(ver.split(".")[:2])
            codename = MACOS_VERSIONS.get(ver_short, "")
            os_name = f"macOS {codename} {real_ver}" if codename else f"macOS {real_ver}"
    elif system == "Linux":
        kernel_ver = platform.release()
        kernel = f"Linux {kernel_ver}"
        os_name = f"{distro.name(pretty=True)}" if distro else system
    else:
        os_name = system
    return os_name, kernel

def get_macos_version():
    try:
        result = subprocess.check_output(
            ["sw_vers", "-productVersion"],
            stderr=subprocess.DEVNULL
        )
        return result.decode().strip()
    except Exception:
        return None

def get_system_info():
    os_name, kernel = get_os_info()
    return {
        'cpu': get_cpu(),
        'ram': get_ram_info(),
        'disks': get_disks_info(),
        'uptime': get_system_uptime(),
        'hostname': platform.node(),
        'os': os_name,
        'kernel': kernel
    }

def main():
    info = get_system_info()
    
    ram = info['ram']
    ram_percent = ram['percent']
    ram_used = ram['used_gb']
    ram_total = ram['total_gb']
    ram_free = ram['free_gb']

    print(f"HOSTNAME: {info['hostname']}")
    print(f"OS: {info['os']}")
    if info['kernel']:
        print(f"KERNEL: {info['kernel']}")
    print(f"CPU: {info['cpu']:.1f}%")
    print(f"RAM: {ram_percent:.1f}% "
          f"({ram_used:.1f} / {ram_total:.1f} GB | Free: {ram_free:.1f} GB)")
    print(f"DISKS:")
    for d in info['disks']:
        print(
            f" - {d['mountpoint']} "
            f"({d['fstype']}): "
            f"{d['percent']:.1f}% "
            f"({d['used_gb']:.1f} / {d['total_gb']:.1f} GB)"
        )
    print(f"UPTIME: {format_seconds(info['uptime'])}")

if __name__ == "__main__":
    main()
