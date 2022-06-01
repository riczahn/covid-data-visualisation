import tkinter as tk

from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from FigureProvider import FigureProvider


class Graph:
    def __init__(self, root, figure_provider: FigureProvider):
        self.root = root
        self.figure_provider = figure_provider
        self.figure = figure_provider.get_de_death_cases_history()
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.canvas.mpl_connect("key_press_event", self.on_key_press)
        self.update()

    def update(self):
        self.canvas.draw()
        self.toolbar.update()

    def pack(self):
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def on_key_press(self, event):
        key_press_handler(event, self.canvas, self.toolbar)

    def load_data(self):
        self.toolbar.pack_forget()
        self.figure = self.figure_provider.get_uk_covid_tests_and_cases()
        self.canvas.figure = self.figure
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)  # todo this solution will throw locking exceptions
        self.update()

