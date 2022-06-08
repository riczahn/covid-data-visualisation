import tkinter as tk

from FigureProvider import FigureProvider
from view.Frame import Frame


class GuiController(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Covid Analysis Tool")
        self.geometry("800x480+400+240")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        figure_provider = FigureProvider()

        self.frames = {}

        # uk graph
        uk_frame = Frame(container, self, figure_provider.get_uk_covid_tests_and_cases())
        self.frames['uk'] = uk_frame

        uk_frame.grid(row=0, column=0, sticky="nsew")

        # de graph
        de_frame = Frame(container, self, figure_provider.get_de_death_cases_history())
        self.frames['de'] = de_frame

        de_frame.grid(row=0, column=0, sticky="nsew")

        self.active_frame = 'uk'
        self.show_frame('uk')

    def next_graph(self):
        if self.active_frame == 'uk':
            self.active_frame = 'de'
            self.show_frame('de')
        else:
            self.active_frame = 'uk'
            self.show_frame('uk')

    def show_frame(self, frame_id):
        frame = self.frames[frame_id]
        frame.tkraise()


if __name__ == '__main__':
    gui = GuiController()
    gui.mainloop()
