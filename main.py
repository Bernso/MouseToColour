import tkinter as tk
from threading import Thread
from PIL import ImageGrab
import pyautogui
from tkcolorpicker import askcolor
import keyboard
from tkinter import filedialog
import os
import requests
import sys
import random

# Creates an icon folder
Icon = "Icon"
if os.path.exists(Icon):
    print("'Icon' folder already exists")
else: 
    print("Creating Icon folder")
    os.makedirs(Icon)
    print("'Icon' folder created")

def download_ico(url, save_path):
    response = requests.get(url) 
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print("ICO file downloaded successfully!")
    else:
        print("Failed to download ICO file.")

url = "https://raw.githubusercontent.com/Bernso/Icons/main/Arhururan.ico"
save_path = os.path.join(Icon, "Arhururan.ico")  # Full file path including directory
download_ico(url, save_path)
print("ICO file download process completed.")


def find_color(color):
    screen = ImageGrab.grab()
    width, height = screen.size
    pixels = screen.load()
    tolerance = 30  # Adjust the tolerance as needed
    for x in range(0, width, 5):  # Step size of 5
        for y in range(0, height, 5):  # Step size of 5
            pixel_color = pixels[x, y]
            # Check if the color matches within the tolerance range
            if all(abs(pixel_color[i] - color[i]) <= tolerance for i in range(3)):
                return x, y
    return None

pyautogui.FAILSAFE = False

class CustomTkinterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Picker & Mouse Mover")
        self.root.geometry("400x210")
        self.root.config(bg="#1f2b3b")  # Darkish blue background color

        # Icon
        self.root.iconbitmap('Icon\\Arhururan.ico')

        self.toggle_flag = False
        self.color_to_find = (255, 0, 0)  

        # Header Label
        self.header_label = tk.Label(root, text="Color Picker & Mouse Mover", font=("Helvetica", 20), bg="#333", fg="white", pady=10)
        self.header_label.pack(fill="x")

        # Color Label
        self.color_label = tk.Label(root, text="Click below to choose a color", font=("Helvetica", 14), bg="white")
        self.color_label.pack(pady=10)

        # Choose Color Button
        self.color_button = tk.Button(root, text="Choose Color", font=("Helvetica", 12), command=self.choose_color)
        self.color_button.pack(pady=10,padx=5)

        # Buttons Frame
        self.buttons_frame = tk.Frame(root, bg="#1f2b3b")  # Set frame background color to match root
        self.buttons_frame.pack(pady=10,padx=5)

        # Start Button
        self.toggle_button = tk.Button(self.buttons_frame, text="Start [F8]", font=("Helvetica", 12), command=self.toggle)
        self.toggle_button.pack(side="left", padx=10)

        # Close App Button
        self.exit_button = tk.Button(self.buttons_frame, text="Close App", font=("Helvetica", 12), command=self.quitv2)
        self.exit_button.pack(side="left", padx=10)

        self.find_color_thread = None

        # Bind F8 key globally to toggle function
        keyboard.on_press_key('f8', self.toggle)
        
        # Bind End key to quitv2 function
        keyboard.on_press_key('end', lambda event: self.quitv2())  # Corrected key binding

    def quitv2(self, event=None):
        print("Thanks for using my product!")
        exit()  

    def toggle(self, event=None):  # Allow for event parameter for key binding
        self.toggle_flag = not self.toggle_flag
        if self.toggle_flag:
            self.toggle_button.config(text="Stop [F8]", bg="#f44336")
            self.color_button.config(state="disabled")
            self.start_moving_mouse()
        else:
            self.toggle_button.config(text="Start [F8]", bg="#4caf50")
            self.color_button.config(state="normal")

    def choose_color(self):
        color = askcolor()
        if color[1]:
            self.color_to_find = color[0]
            self.color_label.config(bg=color[1], text=color[1])

    def start_moving_mouse(self):
        self.find_color_thread = Thread(target=self.find_color_loop)
        self.find_color_thread.daemon = True
        self.find_color_thread.start()

    def find_color_loop(self): 
        while self.toggle_flag:
            position = find_color(self.color_to_find)
            if position:
                # Smoothly move the mouse to the target position
                pyautogui.moveTo(position, duration=0.25)
            #pyautogui.sleep(0.01)

def CustomTkinter():
    root = tk.Tk() 
    app = CustomTkinterApp(root)
    root.mainloop()  

if __name__ == "__main__":
    CustomTkinter()
    for i in range(1, random.randint(1000, 100000)):
        print(f"Why did you not press the close button? {i}")
