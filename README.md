# homelab-monitor 🖥️

A simple system resource monitor written in Python.

Currently, it displays:
- CPU usage
- RAM usage
- Disk usage
- System uptime
- Hostname
- OS name (normalized for Windows/macOS/Linux)
- Kernel (shown on macOS/Linux, hidden on Windows)

The output is shown directly in the terminal.

## Purpose

This project is a small learning and experimentation tool focused on:
- System monitoring
- Python scripting
- Cross-platform system monitoring

## Current Status

🚧 Early development

At the moment:
- Basic monitoring is implemented
- Output is printed to the terminal
- Cross-platform support for Windows, Linux and macOS (lightly tested)
- System uptime is calculated based on OS boot time
- Hostname, OS and kernel information is displayed

## Roadmap (planned)

- Improve disk detection accuracy on Linux and macOS
- Better accuracy to macOS version detection
- Optional JSON output
- Run as a background service
- Code cleanup and small improvements
