import tkinter as tk
from tkinter.constants import *

window = tk.Tk()

frame_navigator = tk.PanedWindow(window, orient=VERTICAL)

frame_navigator.configure(background="white", width=300, height=300)
frame_navigator.pack_propagate(0)

searchbox = tk.Listbox(frame_navigator)
frame_navigator.add(searchbox)

template = tk.Listbox(frame_navigator, exportselection=False)
frame_navigator.add(template)

frame_navigator.pack(side=tk.TOP, expand=1, fill=tk.BOTH)

window.mainloop()