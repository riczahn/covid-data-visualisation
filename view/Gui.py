import tkinter as tk

from FigureProvider import FigureProvider
from view.Frame import Frame


class GuiController(tk.Tk):
    def __init__(self, figures: dict, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Covid Analysis Tool")
        self.geometry("800x480+400+240")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.figure_names = []

        for fig_id, fig in figures.items():
            frame = Frame(container, self, fig)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[fig_id] = frame
            self.figure_names.append(fig_id)

        self.active_frame = self.figure_names[0]
        self.show_frame(self.active_frame)

    def next_graph(self):
        active_id = 0
        for f in self.figure_names:
            if f == self.active_frame:
                break
            active_id = active_id + 1

        next_id = (active_id + 1) % len(self.figure_names)
        self.show_frame(self.figure_names[next_id])

    def show_frame(self, frame_id):
        self.active_frame = frame_id
        frame = self.frames[frame_id]
        frame.tkraise()


if __name__ == '__main__':
    figure_provider = FigureProvider()

    all_figures = {
        'uk': figure_provider.get_uk_covid_tests_and_cases(),
        'de': figure_provider.get_de_death_cases_history()
    }

    gui = GuiController(all_figures)
    gui.mainloop()
