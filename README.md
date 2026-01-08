# homelab-monitor 🖥️

A simple system resource monitor written in Python.

Currently, it displays:
- CPU usage
- RAM usage
- Disk usage
- System uptime
- Hostname
- OS name (normalized for Windows/macOS/Linux)
- Kernel (shown as Darwin on macOS, Linux version on Linux, hidden on Windows)

The output is shown directly in the terminal.

## Purpose

This project is a small learning and experimentation tool focused on:
- System monitoring
- Python scripting
- Cross-platform system monitoring

Built mainly for personal homelab usage and learning purposes.

## Example output

```text
HOSTNAME: Fellipes-Mac-Pro.local
OS: macOS Sequoia 15.7.2
KERNEL: Darwin 24.6.0
CPU: 18.2%
RAM: 50.6% (16.2 / 32.0 GB | Free: 15.8 GB)
DISKS:
 - / (apfs, /dev/disk3s7s1): 6.7% (21.8 / 465.7 GB)
 - /System/Volumes/Data (apfs, /dev/disk3s8): 30.1% (130.7 / 465.7 GB)
 - /System/Volumes/Preboot (apfs, /dev/disk3s2): 2.3% (7.2 / 465.7 GB)
 - /System/Volumes/Update (apfs, /dev/disk3s5): 0.0% (0.1 / 465.7 GB)
 - /System/Volumes/VM (apfs, /dev/disk3s6): 0.0% (0.0 / 465.7 GB)
 - /Volumes/Games (ntfs, /dev/disk2s3): 99.8% (464.8 / 465.7 GB)
UPTIME: 3d 4h 12m
```

## Current Status

🚧 Early development

At the moment:
- Basic monitoring is implemented
- Output is printed to the terminal
- Cross-platform support for Windows, Linux and macOS (lightly tested)
- System uptime is calculated based on OS boot time
- Hostname, OS and kernel information is displayed

## Roadmap (planned)

### Disk improvements
- Improve disk filtering and reduce noisy system mountpoints
- Filter system and ephemeral mountpoints (especially on macOS)
- Display disk labels when available

### General
- Optional JSON output
- Run as a background service
- Code cleanup and small improvements
