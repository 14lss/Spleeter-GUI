import tkinter as tk
import subprocess
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

# Create window
window = tk.Tk(className="Spleeter")
window.title("Spleeter")
window.geometry("382x492")
window.resizable(width=False,height=False)
window.configure(background="#FFFFFF")
window.iconbitmap("spleeter_logo.ico")

# Global variables
filepath = "File Name"

# Class
class Split:
    def __init__(self, filepath):
        self.filepath = filepath
        self.stems = 2

    def get_file_path(self):
        self.filepath = askopenfilename()
        file = self.filepath
        file = file[file.rfind("/") + 1:]
        choose_file_button.config(text=file)

    def set_stems(self, button):
        if button == two_stems_toggle:
            self.stems = 2
            self.set_toggle_color()
        elif button == four_stems_toggle:
            self.stems = 4
            self.set_toggle_color()
        else:
            self.stems = 5
            self.set_toggle_color()

    def set_toggle_color(self):
        if self.stems == 2:
            # On
            two_stems_toggle["bg"] = "#11d075"
            two_stems_toggle["fg"] = "#FFFFFF"
            # Off
            four_stems_toggle["bg"] = "#F7F9FB"
            four_stems_toggle["fg"] = "#000000"
            five_stems_toggle["bg"] = "#F7F9FB"
            five_stems_toggle["fg"] = "#000000"
        elif self.stems == 4:
            # Off
            two_stems_toggle["bg"] = "#F7F9FB"
            two_stems_toggle["fg"] = "#000000"
            # On
            four_stems_toggle["bg"] = "#11d075"
            four_stems_toggle["fg"] = "#FFFFFF"
            # Off
            five_stems_toggle["bg"] = "#F7F9FB"
            five_stems_toggle["fg"] = "#000000"
        else:
            # Off
            two_stems_toggle["bg"] = "#F7F9FB"
            two_stems_toggle["fg"] = "#000000"
            four_stems_toggle["bg"] = "#F7F9FB"
            four_stems_toggle["fg"] = "#000000"
            # On
            five_stems_toggle["bg"] = "#11d075"
            five_stems_toggle["fg"] = "#FFFFFF"

    def split_audio(self):
        if self.filepath == "File Name":
            messagebox.showerror("Error", "No file has been selected")
            return
        if self.filepath[-4:] != ".mp3":
            messagebox.showerror("Error", "Not an mp3 file")
            return
        file = self.filepath
        file = file.replace("/","\\\\")
        subprocess.run(["python", "-mspleeter", "separate", "-oaudio_output", "-pspleeter:"+ str(self.stems) +"stems", file])
    
    def open_settings(self, elements):

        settings_tab["bg"] = "#000000"
        settings_tab["fg"] = "#FFFFFF"
        upload_tab["bg"] = "#F7F9FB"
        upload_tab["fg"] = "#000000"

        self.set_toggle_color()
        
        for element in elements:
            if element == two_stems_toggle:
                element.place(x=16, y=84, width=350, height=110)
            elif element == four_stems_toggle:
                element.place(x=16, y=220, width=350, height=110)
            elif element == five_stems_toggle:
                element.place(x=16, y=356, width=350, height=110)
            else:
                element.place_forget()
        
    def close_settings(self, elements):

        settings_tab["bg"] = "#F7F9FB"
        settings_tab["fg"] = "#000000"
        upload_tab["bg"] = "#000000"
        upload_tab["fg"] = "#FFFFFF"

        for element in elements:
            if element == split_button:
                element.place(x=105, y=442, width=172, height=30)
            elif element == choose_file_button:
                element.place(x=32, y=100, width=318, height=260)
            else:
                element.place_forget()

s = Split(filepath)
# Areas
upload_area = tk.Button(window, text="", state="disabled", bg="#F7F9FB", border=0)
tab_area = tk.Button(window, text="", state="disabled", bg="#F7F9FB", relief="groove")

# Buttons
choose_file_button = tk.Button(window, text="Click to browse", command=s.get_file_path, bg="#E2E6EA", fg="#242634",font=("Inter Regular", 9), relief="groove")
split_button = tk.Button(window, text="Split Audio", command=s.split_audio, font=("Inter Regular", 9), bg="#FFFFFF")

# Settings
two_stems_toggle = tk.Button(window, text="2 Stems (Vocals and accompaniment)", fg="#FFFFFF", command= lambda: s.set_stems(two_stems_toggle), relief="ridge")
four_stems_toggle = tk.Button(window, text="4 Stems (Vocals / drums / bass / other)", fg="#FFFFFF", command= lambda: s.set_stems(four_stems_toggle), relief="ridge")
five_stems_toggle = tk.Button(window, text="5 Stems (Vocals / drums / bass / piano / other)", fg="#FFFFFF", command= lambda: s.set_stems(five_stems_toggle), relief="ridge")

# Tabs
upload_tab = tk.Button(window, text="Upload", bg="#000000", fg="#FFFFFF", font=("Inter Regular", 9), relief="raised",command= lambda: s.close_settings([split_button, choose_file_button, two_stems_toggle, four_stems_toggle, five_stems_toggle]))
settings_tab = tk.Button(window, text="Settings", bg="#F7F9FB", font=("Inter Regular", 9), relief="raised",command= lambda: s.open_settings([split_button, choose_file_button, two_stems_toggle, four_stems_toggle, five_stems_toggle]))

# Load ui
choose_file_button.place(x=32, y=100, width=318, height=260)
split_button.place(x=105, y=442, width=172, height=30)

upload_tab.place(x=97, y=20, width=105, height=28)
settings_tab.place(x=206, y=20, width=78, height=28)

upload_area.place(x=0, y=68, width=382, height=424)
tab_area.place(x=92, y=16, width=197, height=36)

# Keep window open
window.mainloop()
