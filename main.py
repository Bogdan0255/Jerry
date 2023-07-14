import pyautogui
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# Default time interval in seconds
default_interval = 60  # 1 minute

def start_mouse_movement():
    # Disable the start button and enable the stop button
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

    move_mouse()

def stop_mouse_movement():
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

    window.after_cancel(after_id)

def move_mouse():
    # Get the current position of the mouse
    current_x, current_y = pyautogui.position()

    direction = direction_var.get()
    if direction == "Up":
        new_x = current_x
        new_y = current_y - 10
    elif direction == "Down":
        new_x = current_x
        new_y = current_y + 10
    elif direction == "Left":
        new_x = current_x - 10
        new_y = current_y
    elif direction == "Right":
        new_x = current_x + 10
        new_y = current_y
    else:
        new_x = current_x
        new_y = current_y

    # Move the mouse cursor to the new position
    pyautogui.moveTo(new_x, new_y, duration=0.25)  # Adjust the duration as needed

    # Display a message
    status_label.config(text="Mouse moved successfully!")

    # Schedule the next mouse movement
    global after_id
    after_id = window.after(interval.get() * 1000, move_mouse)

def save_settings():
    interval_value = interval.get()
    direction_value = direction_var.get()

    # Perform logic to apply the selected settings
    messagebox.showinfo("Settings Saved", f"Interval: {interval_value} seconds, Direction: {direction_value}")

def exit_application():
    result = messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?")
    if result:
        window.destroy()

# Create the main window
window = tk.Tk()
window.title("That App")

# Set a fixed window size
window.geometry("300x300")

# Use a different theme for a more visually appealing appearance
style = ttk.Style()
style.theme_use("clam")

# Create a menu bar
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

# Create the File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Save", command=save_settings)
file_menu.add_command(label="Exit", command=exit_application)

# Create a settings frame
settings_frame = ttk.LabelFrame(window, text="Settings")
settings_frame.pack(pady=10)

# interval label and entry
interval_label = ttk.Label(settings_frame, text="Mouse Movement Interval (seconds):")
interval_label.pack()
interval = tk.IntVar(value=default_interval)
interval_entry = ttk.Entry(settings_frame, textvariable=interval, width=10)
interval_entry.pack()

# label and dropdown
direction_label = ttk.Label(settings_frame, text="Mouse Movement Direction:")
direction_label.pack()
direction_var = tk.StringVar(value="Down")
direction_dropdown = ttk.Combobox(settings_frame, textvariable=direction_var, values=["Up", "Down", "Left", "Right"])
direction_dropdown.pack()

# status label
status_label = tk.Label(window, text="")
status_label.pack()

button_frame = ttk.Frame(window)
button_frame.pack(pady=10)

# start button
start_button = ttk.Button(button_frame, text="Start", command=start_mouse_movement)
start_button.pack(side=tk.LEFT)

# stop button
stop_button = ttk.Button(button_frame, text="Stop", command=stop_mouse_movement, state=tk.DISABLED)
stop_button.pack(side=tk.LEFT)

# save button
save_button = ttk.Button(window, text="Save", command=save_settings)
save_button.pack()

window.mainloop()
