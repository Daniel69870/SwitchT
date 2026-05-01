import keyboard
import subprocess
import pygetwindow as gw
import time
import os

# === CONFIG ===
STUDY_APPS = [
    "notepad.exe",   # replace with your apps
    "chrome.exe"
]

def minimize_all():
    # Windows shortcut: Win + D (show desktop)
    keyboard.send("windows+d")

def open_study_apps():
    for app in STUDY_APPS:
        try:
            subprocess.Popen(app)
        except Exception as e:
            print(f"Error opening {app}: {e}")

def focus_existing_window(keyword):
    windows = gw.getWindowsWithTitle(keyword)
    if windows:
        try:
            windows[0].activate()
            return True
        except:
            pass
    return False

def panic_switch():
    print("Switching to study mode...")

    minimize_all()
    time.sleep(0.3)

    # Try to focus existing windows first
    if not focus_existing_window("Google Chrome"):
        open_study_apps()

# === HOTKEY ===
keyboard.add_hotkey("shift+f", panic_switch)

print("Running... Press SHIFT+F to switch.")
keyboard.wait()
