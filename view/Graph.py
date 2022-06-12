import tkinter as tk

from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class Graph(tk.Frame):
    def __init__(self, parent, figure: Figure):
        tk.Frame.__init__(self, parent)
        self.figure_modifiers = {}

        self.canvas = FigureCanvasTkAgg(figure, master=self)
        self.canvas.draw()

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()

        self.canvas.mpl_connect("key_press_event", self.on_key_press)

        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

    def on_key_press(self, event):
        key_press_handler(event, self.canvas, self.toolbar)
