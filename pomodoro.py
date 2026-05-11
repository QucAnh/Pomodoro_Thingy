import tkinter as tk
from tkinter import ttk
import customtkinter as ctk 
import time

from asset.icon import play,pause,reset,next,logo



class Pomodoro:
    def __init__(self,root):
        self.root = root
        self.min = 25
        self.rest = 5
        self.total_time = int(self.min * 60)
        self.time_left = self.total_time 
        self.is_running = False
        self.is_rest = False
        self.start_time = None
        
        self.green = "#728F61"
        self.white = "#3F3F43"

        self.playBtn = play(size=(45,45))
        self.pauseBtn = pause(size=(45,45))
        self.nextBtn = next(size=(45,45))
        self.resetBtn = reset(size=(45,45))

        self.build()
    
    def toggle (self):
        self.is_running = not self.is_running

        if self.is_running:          
            self.start_time = time.time() - (self.total_time - self.time_left)
            self.StartBtn.configure(image = self.pauseBtn)
            self.animation()
            self.update_timer()
        else:
            self.StartBtn.configure(image= self.playBtn)
      
    def reset(self,toggle = True):
        self.time_left = self.total_time 
        self.is_running = False
        self.start_time = None
        self.Canvas.itemconfig(self.pie,extent = 0)
        self.StartBtn.configure(image= self.playBtn)
        if toggle:
            self.Canvas.itemconfigure(self.timer_label,text = self.format_time(self.total_time))
    def next(self):
        self.is_rest = not self.is_rest
        if self.is_rest:
            self.total_time = int(self.rest* 60)
            self.reset()

        elif not self.is_rest:
            self.total_time = int(self.min * 60)
            self.reset()

    def format_time (self,seconds):
        return f"{(seconds//60):02}:{(seconds%60):02}"

    def resize(self, event):
        w, h = event.width, event.height
        size = min(w, h) * 0.98

        x1 = (w - size) / 2
        y1 = (h - size ) / 2
        x2 = x1 + size
        y2 = y1 + size 

        tx = (x1 + x2) / 2
        ty = (y1 + y2) / 2       

        self.Canvas.coords(self.circle, x1, y1, x2, y2)
        self.Canvas.coords(self.icircle, x1+24, y1+24, x2-24, y2-24)
        self.Canvas.coords(self.pie, x1, y1, x2, y2)

        self.Canvas.coords(self.timer_label,tx, ty)

    def update_timer (self):
        if not self.is_running: return

        if self.time_left > 0:
            elapsed = time.time() - self.start_time
            self.time_left = self.total_time - elapsed
            self.Canvas.itemconfig(self.timer_label,text=self.format_time(int(self.time_left)))
            self.root.after(33,self.update_timer)
        else:
            self.Canvas.itemconfig(self.timer_label,text="Done !",fill = self.green)
            self.Canvas.itemconfigure(self.circle,fill = self.green)
            self.is_running = False
            self.reset(toggle=False)

    def animation (self):
        if not self.is_running : return

        # elapsed time
        elapsed = time.time() - self.start_time

        # progress (0 → 1)
        progress = elapsed / self.total_time

        # clamp
        if progress > 1:
            progress = 1

        # smooth angle (float)
        angle = 360 * progress

        self.Canvas.itemconfig(self.pie, extent=angle)

        # keep updating
        self.root.after(33, self.animation)   # ~60 FPS
    
    def status_on_click(self):

        pass

    def build (self):
        ## Canvas
        bg_color = self.root._apply_appearance_mode(
            self.root.cget("fg_color")
        )
        self.Canvas = ctk.CTkCanvas(self.root,highlightthickness=0,background = bg_color)
        self.Canvas.pack(fill="both", expand=True)

        self.circle = self.Canvas.create_oval(0, 0, 0, 0, fill = self.white,outline ="")
        self.pie = self.Canvas.create_arc(0, 0, 0, 0, start=90, extent=0, fill="#AAB1BE",outline ="")
        self.icircle = self.Canvas.create_oval(0, 0, 0, 0, fill=bg_color,outline ="")

        self.Canvas.bind("<Configure>", self.resize)

        ## Timer
        self.timer_label = self.Canvas.create_text(0,0,text=self.format_time(self.total_time), font=("Arial", 50),fill="white",anchor="center")

        ##Status
        self.status = ctk.CTkLabel(self.root,text="Pomodoro",font=("Arial",32,"bold"),text_color="white",corner_radius=40)
        self.status.pack(pady=30,ipady=10,ipadx=10)

        self.status.bind("<Enter>",lambda e: self.status.configure(fg_color="#353B44"))
        self.status.bind("<Leave>",lambda e: self.status.configure(fg_color="transparent"))
        self.status.bind("<Button-1>",self.status_on_click)

        ## Control
        self.control = ctk.CTkFrame(self.root,fg_color=None)
        self.control.pack(pady = (10,60),fill="x")
        self.control.grid_columnconfigure((0,1,2),weight=1)
        # self.control.grid_rowconfigure((0,1,2),weight=1)

        self.ResetBtn = ctk.CTkButton(self.control, image=self.resetBtn,fg_color=("gray86", "gray17") , text="", command=self.reset,height=100)
        self.ResetBtn.grid(row = 0, column = 0,sticky="nsew")

        self.StartBtn = ctk.CTkButton(self.control,image=self.playBtn ,fg_color=("gray86", "gray17") , text="", command=self.toggle)
        self.StartBtn.grid(row = 0, column = 1,sticky="nsew")

        self.NextBtn = ctk.CTkButton(self.control, image=self.nextBtn,fg_color=("gray86", "gray17") , text="", command=self.next)
        self.NextBtn.grid(row = 0, column = 2,sticky="nsew")

#####################################################################
##create window 
root = ctk.CTk()

root.title("Pomodoro App")
root.iconphoto(True,logo())
root.geometry("750x800")    

root.grid_rowconfigure(0,weight=1)

root.grid_columnconfigure((0,1,2),weight = 1)

col1 = ctk.CTkFrame(root,fg_color=None)
col1.grid(sticky="nsew",row=0,column=0)
col2 = ctk.CTkFrame(root,fg_color=None)
col2.grid(sticky="nsew",row=0,column=1)
col3 = ctk.CTkFrame(root,fg_color=None)
col3.grid(sticky="nsew",row=0,column=2)

app = Pomodoro(col2)

##keep window open
root.mainloop()