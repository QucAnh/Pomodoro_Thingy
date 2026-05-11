from PIL import Image
import os
import customtkinter as ctk
import tkinter as tk

# Base path relative to this file
BASE = os.path.dirname(__file__)

def load(name: str, size=(30,30)) -> ctk.CTkImage:
    path = os.path.join(BASE, name)
    return ctk.CTkImage(Image.open(path), size=size)

def Load(name: str) -> tk.PhotoImage:
    path = os.path.join(BASE,name)
    return tk.PhotoImage(file=path)

# Pre-load Logo
logo = lambda: Load("pomodoro_icon.png")

# Pre-load all icons
play  = lambda size=(30,30): load("play.png",  size)
pause = lambda size=(30,30): load("stop.png", size)
reset = lambda size=(30,30): load("reset.png",size)
next  = lambda size=(30,30): load("next.png",  size)
