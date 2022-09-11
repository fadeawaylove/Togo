import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame

app = ttk.Window()

sf = ScrolledFrame(app, autohide=True)
sf.pack(fill=BOTH, expand=YES, padx=10, pady=10)

# add a large number of checkbuttons into the scrolled frame
for x in range(20):
    ttk.Checkbutton(sf, text=f"Checkbutton {x}").pack(anchor=W)

app.mainloop()