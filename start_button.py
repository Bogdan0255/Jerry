import pyautogui
import tkinter as tk

def start_mouse_movement(window, start_button, stop_button, interval, star_size):
    # Disable the start button and enable the stop button
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

    move_mouse(window, interval, star_size)

def move_mouse(window, interval, star_size):
    # Enable the start button and disable the stop and click buttons
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    click_button.config(state=tk.DISABLED)

    # Cancel the scheduled mouse movement
    window.after_cancel(after_id)

def stop_mouse_movement(window, start_button, stop_button, after_id):
    # Enable the start button and disable the stop button
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

    # Cancel the scheduled mouse movement
    window.after_cancel(after_id)
