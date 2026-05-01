import keyboard
import subprocess
import pygetwindow as gw
import time
import json
import tkinter as tk
from tkinter import filedialog, messagebox

CONFIG_FILE = "config.json"

# === DEFAULT CONFIG ===
config = {
    "hotkey": "shift+f",
    "apps": ["notepad.exe", "chrome.exe"]
}

# === LOAD CONFIG ===
def load_config():
    global config
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
    except:
        pass

def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

# === FUNCTIONALITY ===
def minimize_all():
    keyboard.send("windows+d")

def open_apps():
    for app in config["apps"]:
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

    if not focus_existing_window("Chrome"):
        open_apps()

# === HOTKEY SETUP ===
def apply_hotkey():
    keyboard.unhook_all_hotkeys()
    try:
        keyboard.add_hotkey(config["hotkey"], panic_switch)
        status_label.config(text=f"Hotkey set: {config['hotkey']}")
    except:
        messagebox.showerror("Error", "Invalid hotkey")

# === UI ===
def add_app():
    file_path = filedialog.askopenfilename()
    if file_path:
        config["apps"].append(file_path)
        app_list.insert(tk.END, file_path)

def remove_app():
    selected = app_list.curselection()
    if selected:
        index = selected[0]
        config["apps"].pop(index)
        app_list.delete(index)

def update_hotkey():
    config["hotkey"] = hotkey_entry.get()
    apply_hotkey()

def save_all():
    save_config()
    messagebox.showinfo("Saved", "Configuration saved!")

# === BUILD UI ===
load_config()

root = tk.Tk()
root.title("Panic Switch Config")
root.geometry("400x400")

# Hotkey
tk.Label(root, text="Hotkey:").pack()
hotkey_entry = tk.Entry(root)
hotkey_entry.insert(0, config["hotkey"])
hotkey_entry.pack()

tk.Button(root, text="Apply Hotkey", command=update_hotkey).pack(pady=5)

# Apps list
tk.Label(root, text="Applications:").pack()

app_list = tk.Listbox(root)
app_list.pack(fill=tk.BOTH, expand=True)

for app in config["apps"]:
    app_list.insert(tk.END, app)

tk.Button(root, text="Add App", command=add_app).pack(pady=2)
tk.Button(root, text="Remove Selected", command=remove_app).pack(pady=2)

# Save
tk.Button(root, text="Save Config", command=save_all).pack(pady=10)

# Status
status_label = tk.Label(root, text="")
status_label.pack()

apply_hotkey()

print("Running in background...")

root.mainloop()
