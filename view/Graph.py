import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from main import build_graph


class Graph:
    def __init__(self, root):
        self.figure = build_graph()
        self.root = root
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.canvas.mpl_connect("key_press_event", self.on_key_press)

    def draw(self):
        self.canvas.draw()
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def on_key_press(self, event):
        print("you pressed {}".format(event.key))
        key_press_handler(event, self.canvas, self.toolbar)
