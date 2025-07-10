import os
import subprocess
import time
import threading
import tkinter as tk
from tkinter import filedialog
import psutil

running = False

# Function to check if a process is running
def is_process_running(name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() == name.lower():
            return True
    return False

# Function to start the program
def start_program(exe_path, label_status, label_countdown):
    global running
    running = True

# Function to launch the SKSE executable and monitor Skyrim
    def loop():
        while running:
            try:
                if is_process_running("SkyrimSE.exe"):
                    label_status.config(bg="green", text="Skyrim is already running")
                    time.sleep(5)
                    continue

                exe_dir = os.path.dirname(exe_path)
                process = subprocess.Popen(
                    [exe_path],
                    cwd=exe_dir,
                    shell=True
                )
                # Update status to indicate SKSE is launched
                label_status.config(bg="yellow", text="SKSE Successfully Launched")

                # Wait for Skyrim to open
                while running and not is_process_running("SkyrimSE.exe"):
                    time.sleep(1)
                # Update status to indicate Skyrim is running
                label_status.config(bg="green", text="Skyrim is running")

                # Wait for Skyrim to close
                while running and is_process_running("SkyrimSE.exe"):
                    time.sleep(1)

                if not running:
                    break

                # Restart countdown
                # Update status to indicate Skyrim is closed
                label_status.config(bg="red", text="Skyrim is closed")
                for i in range(5, 0, -1):
                    label_countdown.config(text=f"Restarting in: {i} seconds")
                    time.sleep(1)

            except Exception as e:
                # Update status to indicate an error occurred
                label_status.config(bg="orange", text=f"ERROR: {str(e)}")
                break

        label_countdown.config(text="Stopped.")

    t = threading.Thread(target=loop)
    t.daemon = True
    t.start()

# Function to stop the program
def stop_program():
    global running
    running = False

# Function to browse and select the SKSE executable file
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
    entry_exe_path.delete(0, tk.END)
    entry_exe_path.insert(0, file_path)

# GUI
# Create the main window
root = tk.Tk()
root.resizable(False, False)
root.title("SkyrimSE Auto Launcher")
root.geometry("400x200")

# Status label
label_status = tk.Label(root, text="Status", bg="gray", width=30)
label_status.pack(side="top", fill="x", padx=10, pady=10)

# Entry box for the SKSE executable path
entry_exe_path = tk.Entry(root, width=100, bg="white", fg="black")
entry_exe_path.pack(pady=10, padx=10)

# Button to browse for the SKSE executable
btn_browse = tk.Button(root, text="Select SKSE", command=browse_file)
btn_browse.pack(pady=5, padx=10)

# Countdown label
label_countdown = tk.Label(root, text="", width=30)
label_countdown.pack(pady=10, padx=10)

# Start button
btn_start = tk.Button(root, text="Start", width=25, command=lambda: start_program(entry_exe_path.get(), label_status, label_countdown))
btn_start.pack(side="right", anchor="se", padx=10, pady=10)

# Stop button
btn_stop = tk.Button(root, text="Stop", width=25,command=stop_program)
btn_stop.pack(side="left", anchor="se", padx=10, pady=10)

root.mainloop()
