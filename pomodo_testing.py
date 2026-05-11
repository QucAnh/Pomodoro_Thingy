import tkinter as tk
from tkinter   import ttk
import customtkinter as ctk
import random as ran
import math
import time

root = tk.Tk()

root.title("Testing")
root.geometry("500x800")

label = tk.Label(text="Counter", fg="black",font=32)
label.pack()

count = tk.IntVar(value="0")
counter = ttk.Label(root,text=count.get(),font=("Arial", 32),foreground="blue")
counter.pack()

def click():
    count.set(count.get() + 1)
    counter.config(text=count.get())

button = ttk.Button(root,text="click",command=click)
button.pack()
###########################
# labels.config(text="New Text")
framer = tk.Frame(root, bd = 2,relief="solid" ,bg="yellow")
framer.pack(pady=24)

entry = ttk.Entry(framer)
entry.grid(row=0,column=0,padx=8)

output  = tk.Label(root,text="",font=64,bd=1,relief="flat",bg="pink")
output.pack(pady=24,fill="x")

def show_text():
    values = entry.get()
    print(values)
    output.config(text=values)
    entry.delete(0,tk.END)

button = ttk.Button(framer, text="Get Input", command=show_text)
button.grid(row=0,column=1,padx=8)

ctk.CTkButton(framer, text="A",corner_radius=25,fg_color="red",command=("active","white")).grid(row=1, column=0, padx=10, pady=10)
style = ttk.Style()
style.configure("My.TButton")
style.map("My.TButton",
    foreground=[
        ("pressed", "red"),
        ("active", "blue")
    ],
    background=[
        ("pressed", "yellow"),
        ("active", "pink")
    ]
)
ttk.Button(framer, text="B",style = "My.TButton").grid(row=1, column=1, padx=10, pady=10)

def on_key_entry(event):
    print("key",event.keysym," pressed")
    entry.focus()
    entry.select_range(0,tk.END)

root.bind("/",on_key_entry)

def on_key_summit(event):
    print("key",event.keysym," pressed")
    show_text()

root.bind("<Return>",on_key_summit)

def click(event):
    print("x - ",event.x,"|| y - ",event.y)
    widget = event.widget

    if widget != entry :
        root.focus()


root.bind("<Button-1>",click)

bar = ttk.Progressbar(root, length=200, mode="determinate")
bar.pack()

bar["value"] = 50

def new_window():
    child = tk.Tk()
    bar = ttk.Progressbar(child, length=200, mode="determinate")
    bar.pack()
    bar["value"] = 10
    child.mainloop()
############################################################

shape = tk.Canvas(root,height=500,width=500,bg="pink")
shape.pack(padx=10,pady=10)

circle = shape.create_oval(450, 450, 50, 50, fill="blue")


pie = shape.create_arc(
    450, 450, 50, 50,
    start=-90,
    extent=0,
    style="pieslice",
    fill="red",
    outline =""
)

fill = 0
color = ["red","white","yellow","pink","black","purple","orange"]
state = False

start_time = None

def animation():
    global state, start_time

    if not state:
        return

    # elapsed time
    elapsed = time.time() - start_time

    # progress (0 → 1)
    progress = elapsed / total_time

    # clamp
    if progress > 1:
        progress = 1

    # smooth angle (float, not int!)
    angle = 360 * progress
    print(angle)

    shape.itemconfig(pie, extent=angle)

    # keep updating at high frequency
    root.after(16, animation)   # ~60 FPS

def toggle():
    global state, start_time

    state = not state

    if state:
        start_time = time.time() - (total_time - time_left)
        animation()
        update_timer()
        
minute = 25
time_left = int(60*minute)
total_time = time_left

def format_time(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02}:{secs:02}"

def update_timer():
    global time_left, state
    if not state: return
    if time_left > 0:
        time_left -= 1
        print("time: ",time_left)
        timer_label.configure(text=format_time(time_left))
        root.after(1000, update_timer)
    elif time_left == 0:
        timer_label.configure(text="Done!")
        # shape.itemconfig(pie, extent=360)  # ensure perfect finish

        state = False
    
timer_label = ctk.CTkLabel(root,text=f"{math.floor(minute):02}" + ":00",font=("arial",40),bg_color="green")
timer_label.pack()
ctk.CTkButton(root,text="Click me",command=toggle).pack()





root.mainloop()