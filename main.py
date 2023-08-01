import pyautogui
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
from start_button import start_mouse_movement, stop_mouse_movement
import json

# fail test disable + time define
pyautogui.FAILSAFE = False
default_interval = 60  # in seconds

# Config path
config_file = "config.json"

# Define the star size
star_size = 25


def start_mouse_movement():
    # Disable the start button and enable the stop and click buttons
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    click_button.config(state=tk.NORMAL)

    # Save the initial position of the cursor
    global initial_x, initial_y
    initial_x, initial_y = pyautogui.position()

    move_mouse()


def stop_mouse_movement():
    # Enable the start button and disable the stop and click buttons
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    click_button.config(state=tk.DISABLED)

    # Cancel the scheduled mouse movement
    window.after_cancel(after_id)


def perform_left_click():
    # Perform a left click at the current mouse position
    pyautogui.click()


def move_mouse():
    if stationary_checkbox_var.get():
        # Perform the circle thing at the current mouse position
        pyautogui.moveTo(initial_x + star_size, initial_y, duration=0.25, tween=pyautogui.easeInOutQuad)
        pyautogui.dragRel(star_size, star_size, duration=0.1)
        pyautogui.dragRel(-star_size, star_size, duration=0.1)
        pyautogui.dragRel(-star_size, -star_size, duration=0.1)
        pyautogui.dragRel(star_size, -star_size, duration=0.1)
        pyautogui.dragRel(star_size, star_size, duration=0.1)
    else:
        # Get the current position of the mouse
        current_x, current_y = pyautogui.position()

        # Get the selected direction
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
            # No direction selected, stay in place
            new_x = current_x
            new_y = current_y

        # Calculate the star size
        star_radius = star_size // 2

        # Draw the star at the new position
        pyautogui.moveTo(new_x, new_y, duration=0.25, tween=pyautogui.easeInOutQuad)
        pyautogui.dragRel(star_radius, star_radius, duration=0.1)
        pyautogui.dragRel(-star_radius, star_radius, duration=0.1)
        pyautogui.dragRel(-star_radius, -star_radius, duration=0.1)
        pyautogui.dragRel(star_radius, -star_radius, duration=0.1)
        pyautogui.dragRel(star_radius, star_radius, duration=0.1)

    # Display message
    status_label.config(text="Mouse moved successfully!")

    # Schedule the next mouse movement
    global after_id
    after_id = window.after(interval.get() * 1000, move_mouse)

    # Move the cursor back to its initial position
    pyautogui.moveTo(initial_x, initial_y, duration=0.25, tween=pyautogui.easeInOutQuad)


def save_settings():
    interval_value = interval.get()
    direction_value = direction_var.get()

    # Create a settings dictionary
    settings = {
        "interval": interval_value,
        "direction": direction_value
    }

    try:
        # Save the settings to the configuration file
        with open(config_file, "w") as file:
            json.dump(settings, file)

        messagebox.showinfo("Settings Saved", "Settings saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save settings.\n\nError: {str(e)}")


def load_settings():
    try:
        # Load the settings from the configuration file
        with open(config_file, "r") as file:
            settings = json.load(file)

        # Set the loaded values for interval and direction
        interval.set(settings["interval"])
        direction_var.set(settings["direction"])

        messagebox.showinfo("Settings Loaded", "Settings loaded successfully.")
    except FileNotFoundError:
        messagebox.showwarning("Warning", "No saved settings found.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load settings.\n\nError: {str(e)}")


def show_help():
    help_text = '''
    Mouse Mover App Help

    - Use the Settings section to set the mouse movement interval and direction.
    - Check the "Stationary" option to keep the mouse stationary and only perform the circle thing.
    - Click the Start button to begin the mouse movement or left click action.
    - The mouse will move in the selected direction based on the specified interval.
    - Click the Stop button to stop the mouse movement or left click action.
    - You can save and load settings using the File menu.

    For further assistance, please contact our support team.
    '''

    help_window = tk.Toplevel(window)
    help_window.title("Help")
    help_window.geometry("400x300")

    help_textbox = scrolledtext.ScrolledText(help_window, width=60, height=15, wrap=tk.WORD)
    help_textbox.pack(fill=tk.BOTH, expand=True)

    help_textbox.insert(tk.INSERT, help_text)
    help_textbox.configure(state=tk.DISABLED)


# Create the main window
window = tk.Tk()
window.title("Jerry's app")

# Set the window icon
window.iconbitmap("C:\\Users\\bogdan.DESKTOP-4CRLMLK\\PycharmProjects\\mover231\\icon.ico") # Replace "path_to_icon.ico" with the path to your icon file

window.geometry("300x300")

style = ttk.Style()
style.theme_use("clam")

# Create a menu bar
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

# Create the File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Save", command=save_settings)
file_menu.add_command(label="Load", command=load_settings)
file_menu.add_command(label="Exit", command=window.quit)

# Create the Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=show_help)

settings_frame = ttk.LabelFrame(window, text="Settings")
settings_frame.pack(pady=10)

interval_label = ttk.Label(settings_frame, text="Mouse Movement Interval (seconds):")
interval_label.pack()
interval = tk.IntVar(value=default_interval)
interval_entry = ttk.Entry(settings_frame, textvariable=interval, width=10)
interval_entry.pack()

direction_label = ttk.Label(settings_frame, text="Mouse Movement Direction:")
direction_label.pack()
direction_var = tk.StringVar()
direction_dropdown = ttk.Combobox(settings_frame, textvariable=direction_var,
                                  values=["", "Up", "Down", "Left", "Right"])
direction_dropdown.pack()

# Create the stationary checkbox
stationary_checkbox_var = tk.BooleanVar()
stationary_checkbox = ttk.Checkbutton(settings_frame, text="Stationary (Circle Only)", variable=stationary_checkbox_var)
stationary_checkbox.pack()

# Create a status label
status_label = tk.Label(window, text="")
status_label.pack()

# Create a frame to hold the buttons
button_frame = ttk.Frame(window)
button_frame.pack(pady=10)

# Create the start button
start_button = ttk.Button(button_frame, text="Start", command=start_mouse_movement)
start_button.pack(side=tk.LEFT)

# Create the stop button
stop_button = ttk.Button(button_frame, text="Stop", command=stop_mouse_movement, state=tk.DISABLED)
stop_button.pack(side=tk.LEFT)

# Create the click button
click_button = ttk.Button(button_frame, text="Left Click", command=perform_left_click, state=tk.DISABLED)
click_button.pack(side=tk.LEFT)

window.mainloop()
