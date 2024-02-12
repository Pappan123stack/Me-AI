import tkinter as tk
from datetime import datetime
import pyttsx3
import threading

def update_time_label():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_label.config(text=current_time)
    time_label.after(1000, update_time_label)

def set_reminder():
    reminder_time = e1.get()
    reminder_msg = e2.get()
    reminders[reminder_time] = reminder_msg
    reminder_label.config(text=f"Reminder set for {reminder_time}: {reminder_msg}")

def check_reminders():
    current_time = datetime.now().strftime("%H:%M")
    for reminder_time, message in list(reminders.items()):
        if current_time == reminder_time:
            threading.Thread(target=show_reminder, args=(message,)).start()
            speak(message)
            del reminders[reminder_time]
    root.after(60000, check_reminders)

def show_reminder(message):
    popup = tk.Toplevel(root)
    popup.title("Reminder")
    popup.attributes('-topmost', True)  # Make the popup appear above other windows
    reminder_text = tk.Label(popup, text=message, font=("Helvetica", 16), fg="red")
    reminder_text.pack()
    tk.Button(popup, text="Ok", command=popup.destroy).pack()
    blink(reminder_text)

def blink(label):
    current_color = label.cget("foreground")
    next_color = "red" if current_color != "red" else "white"
    label.config(foreground=next_color)
    label.after(500, lambda: blink(label))

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

root = tk.Tk()
root.title("Reminder App")

reminders = {}

time_label = tk.Label(root, font=('Helvetica', 16))
time_label.pack()
update_time_label()

tk.Label(root, text="Set Reminder Time (HH:MM)").pack()
e1 = tk.Entry(root)
e1.pack()

tk.Label(root, text="Reminder Message").pack()
e2 = tk.Entry(root)
e2.pack()

set_button = tk.Button(root, text="Set Reminder", command=set_reminder)
set_button.pack()

reminder_label = tk.Label(root, text="")
reminder_label.pack()

root.after(60000, check_reminders)

root.mainloop()
