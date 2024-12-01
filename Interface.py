import tkinter as tk
from tkinter import filedialog
import configparser
import Functions
from Functions import start_game

def select_file(section, key):

    file_path = filedialog.askopenfilename()
    if file_path:

        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        if section not in config:
            config[section] = {}
        config[section][key] = file_path

        with open('config.ini', 'w', encoding='utf-8') as configfile:
            config.write(configfile)
        if key == "file_path":
            label_file_path.config(text=f"beatmap selected")
        elif key == "osu_exe_path":
            label_osu_exe.config(text=f"Osu!path selected")



root = tk.Tk()
root.title("File Selector")
root.geometry("600x350") 

root.resizable(False, False)

frame = tk.Frame(root)
frame.pack(pady=20, fill="x") 

frame2 = tk.Frame(root)
frame2.pack(pady=20, fill="x")

frame3 = tk.Frame(root)
frame3.pack(pady=20, fill="x")

font = ('Arial', 12, 'bold') 


label_description_osu_exe = tk.Label(frame, text="Select an osu!.exe: ", font=font, anchor="w")
label_description_osu_exe.pack(side="left", padx=10, pady=10)

label_osu_exe = tk.Label(frame, text="No file selected", wraplength=400)
label_osu_exe.pack(side="left", padx=10, pady=10, expand=True)

btn_select_osu_exe = tk.Button(frame, text="SELECT", command=lambda: select_file('Settings', 'osu_exe_path'), width=20, height=3)
btn_select_osu_exe.pack(side="right", padx=10)

label_description_beatmap = tk.Label(frame2, text="Select osu!beatmap: ", font=font, anchor="w")
label_description_beatmap.pack(side="left", padx=10, pady=10)

label_file_path = tk.Label(frame2, text="No file selected", wraplength=400)
label_file_path.pack(side="left", padx=10, pady=10, expand=True)

btn_select_beatmap = tk.Button(frame2, text="SELECT", command=lambda: select_file('Settings', 'file_path'), width=20, height=3)
btn_select_beatmap.pack(side="right", padx=10)

play_button = tk.Button(frame3, text='Play!',command=start_game, width=20, height=3)
play_button.pack(side='bottom', padx=10)

if __name__ == '__main__':
    root.mainloop()
