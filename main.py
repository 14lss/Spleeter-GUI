import tkinter as tk
import subprocess
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

# Create window
window = tk.Tk(className="Spleeter")
window.geometry("382x492")
window.resizable(width=False,height=False)
window.configure(background="#FFFFFF")

# Global variables
filepath = "File Name"

# Class
class Split:
    def __init__(self, filepath):
        self.filepath = filepath

    def get_file_path(self):
        self.filepath = askopenfilename()
        file = self.filepath
        file = file[file.rfind("/") + 1:]
        choose_file_button.config(text=file)

    def split_audio(self):
        if self.filepath == "File Name":
            messagebox.showerror("Error", "No file has been selected")
            return
        if self.filepath[-4:] != ".mp3":
            messagebox.showerror("Error", "Not an mp3 file")
            return
        file = self.filepath
        file = file.replace("/","\\\\")
        subprocess.run(["python", "-mspleeter", "separate", "-oaudio_output", "-pspleeter:4stems", file])
    
    def open_settings(self, elements):
        for element in elements:
            element.place_forget()
        
    def close_settings(self, elements):
        for element in elements:
            if element["text"] == "Split Audio":
                element.place(x=105, y=442, width=172, height=30)
            else:
                element.place(x=32, y=100, width=318, height=260)

s = Split(filepath)

# Areas
upload_area = tk.Button(window, text="", state="disabled", bg="#F7F9FB", border=0)
tab_area = tk.Button(window, text="", state="disabled", bg="#F7F9FB", relief="groove")

# Buttons
choose_file_button = tk.Button(window, text="Click to browse", command=s.get_file_path, bg="#E2E6EA", fg="#242634",font=("Inter Regular", 9), relief="groove")
split_button = tk.Button(window, text="Split Audio", command=s.split_audio, font=("Inter Regular", 9), bg="#FFFFFF")

# Tabs
upload_tab = tk.Button(window, text="Upload", bg="#000000", fg="#FFFFFF", font=("Inter Regular", 9), command= lambda: s.close_settings([split_button, choose_file_button]))
settings_tab = tk.Button(window, text="Settings", bg="#F7F9FB", font=("Inter Regular", 9), command= lambda: s.open_settings([split_button, choose_file_button]))

# Load ui
choose_file_button.place(x=32, y=100, width=318, height=260)

split_button.place(x=105, y=442, width=172, height=30)

upload_tab.place(x=97, y=20, width=105, height=28)

settings_tab.place(x=206, y=20, width=78, height=28)

upload_area.place(x=0, y=68, width=382, height=424)

tab_area.place(x=92, y=16, width=197, height=36)
#file_name_label.pack()


# Keep window open
window.mainloop()