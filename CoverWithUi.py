import keyboard
import subprocess
import pygetwindow as gw
import json
import tkinter as tk
from tkinter import filedialog, messagebox

CONFIG_FILE = "config.json"

config = {
    "hotkey": "shift+f",
    "hide_apps": [],
    "show_apps": ["notepad.exe"]
}

current_hotkey = None

# === LOAD / SAVE ===
def load_config():
    global config
    try:
        with open(CONFIG_FILE, "r") as f:
            loaded = json.load(f)

        config["hotkey"] = loaded.get("hotkey", config["hotkey"])
        config["hide_apps"] = loaded.get("hide_apps", [])
        config["show_apps"] = loaded.get("show_apps", loaded.get("apps", config["show_apps"]))
    except:
        pass

def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

# === WINDOW CONTROL ===
def find_window(keyword):
    for w in gw.getAllWindows():
        if keyword.lower() in w.title.lower():
            return w
    return None

def focus_maximize(keyword):
    win = find_window(keyword)
    if win:
        try:
            win.restore()
            win.activate()
            win.maximize()
            return True
        except:
            pass
    return False

def minimize_window(keyword):
    win = find_window(keyword)
    if win:
        try:
            win.minimize()
        except:
            pass

# === CORE ===
def minimize_all():
    keyboard.send("windows+d")

def open_app(app):
    try:
        subprocess.Popen(app)
    except:
        pass

def panic_switch():
    print("Switching mode...")

    minimize_all()

    for app in config["hide_apps"]:
        minimize_window(app.replace(".exe", ""))

    for app in config["show_apps"]:
        name = app.replace(".exe", "")
        if not focus_maximize(name):
            open_app(app)

# === HOTKEY ===
def apply_hotkey():
    global current_hotkey

    if current_hotkey:
        try:
            keyboard.remove_hotkey(current_hotkey)
        except:
            pass

    try:
        current_hotkey = keyboard.add_hotkey(config["hotkey"], panic_switch)
        status_label.config(text=f"Hotkey: {config['hotkey']}")
    except:
        messagebox.showerror("Error", "Invalid hotkey")

# === MOVE LOGIC ===
def move_to_hide():
    sel = show_list.curselection()
    if sel:
        i = sel[0]
        item = config["show_apps"].pop(i)
        config["hide_apps"].append(item)
        refresh_lists()

def move_to_show():
    sel = hide_list.curselection()
    if sel:
        i = sel[0]
        item = config["hide_apps"].pop(i)
        config["show_apps"].append(item)
        refresh_lists()

def refresh_lists():
    hide_list.delete(0, tk.END)
    for app in config["hide_apps"]:
        hide_list.insert(tk.END, app)

    show_list.delete(0, tk.END)
    for app in config["show_apps"]:
        show_list.insert(tk.END, app)

# === UI ACTIONS ===
def add_hide():
    f = filedialog.askopenfilename()
    if f:
        config["hide_apps"].append(f)
        refresh_lists()

def add_show():
    f = filedialog.askopenfilename()
    if f:
        config["show_apps"].append(f)
        refresh_lists()

def remove_hide():
    sel = hide_list.curselection()
    if sel:
        config["hide_apps"].pop(sel[0])
        refresh_lists()

def remove_show():
    sel = show_list.curselection()
    if sel:
        config["show_apps"].pop(sel[0])
        refresh_lists()

def update_hotkey():
    config["hotkey"] = hotkey_entry.get()
    apply_hotkey()

def save_all():
    save_config()
    messagebox.showinfo("Saved", "Config saved!")

# === UI ===
load_config()

root = tk.Tk()
root.title("Mode Switch Tool")
root.geometry("550x450")

# HOTKEY
tk.Label(root, text="Hotkey").pack()

hotkey_entry = tk.Entry(root)
hotkey_entry.insert(0, config["hotkey"])
hotkey_entry.pack()

tk.Button(root, text="Apply Hotkey", command=update_hotkey).pack(pady=5)

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# LEFT
left = tk.Frame(frame)
left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

tk.Label(left, text="Hide Apps").pack()

hide_list = tk.Listbox(left)
hide_list.pack(fill=tk.BOTH, expand=True)

tk.Button(left, text="Add", command=add_hide).pack()
tk.Button(left, text="Remove", command=remove_hide).pack()

# CENTER BUTTONS
center = tk.Frame(frame)
center.pack(side=tk.LEFT, fill=tk.Y)

tk.Button(center, text="→ Move to Hide", command=move_to_hide).pack(pady=10)
tk.Button(center, text="← Move to Show", command=move_to_show).pack(pady=10)

# RIGHT
right = tk.Frame(frame)
right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

tk.Label(right, text="Show Apps").pack()

show_list = tk.Listbox(right)
show_list.pack(fill=tk.BOTH, expand=True)

tk.Button(right, text="Add", command=add_show).pack()
tk.Button(right, text="Remove", command=remove_show).pack()

# SAVE
tk.Button(root, text="Save Config", command=save_all).pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack()

refresh_lists()
apply_hotkey()

print("Running...")
root.mainloop()
