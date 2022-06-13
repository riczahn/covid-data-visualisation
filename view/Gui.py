import tkinter as tk

import Constants
from FigureProvider import FigureProvider
from Lockdown import events, lockdowns
from exception.InvalidParameterException import InvalidParameterException
from view.Frame import Frame
from view.Sidebar import Sidebar


class GuiController(tk.Tk):

    def __init__(self, figures: dict, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Covid Analysis Tool")

        container = tk.Frame(self)
        container.grid(row=0, column=0, sticky="n")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.figure_names = list(figures.keys())
        self.active_frame = self.figure_names[0]

        for fig_id, fig in figures.items():
            frame = Frame(container, fig)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[fig_id] = frame

        self.sidebar = Sidebar(self, self)
        self.sidebar.grid(row=0, column=1, sticky="n")

        self.show_frame(self.active_frame)

    def show_frame(self, frame_id):
        self.active_frame = frame_id
        frame = self.frames[frame_id]
        frame.tkraise()

    def get_all_graphs(self):
        return self.figure_names

    def get_current_graph(self):
        return self.active_frame

    def show_covid_events(self, action):
        frame = self.frames[self.active_frame]

        if action == Constants.TOGGLE_ACTIVE:
            axes = frame.graph.canvas.figure.get_axes()[0]
            lines = axes.vlines(list(events.keys()), 0, 1, transform=axes.get_xaxis_transform(), colors='r',
                                linestyles='dashed')
            frame.graph.figure_modifiers['covid_event_lines'] = lines
        elif action == Constants.TOGGLE_INACTIVE:
            frame.graph.figure_modifiers['covid_event_lines'].remove()
        else:
            raise InvalidParameterException(f'Unsupported action type {action}')

        frame.graph.canvas.draw()

    def show_lockdowns(self, action):
        frame = self.frames[self.active_frame]
        axes = frame.graph.canvas.figure.get_axes()[0]

        if action == Constants.TOGGLE_ACTIVE:
            frame.graph.figure_modifiers['lockdowns'] = []

            for lockdown in lockdowns.values():
                start_date = lockdown['start_date']
                end_date = lockdown['end_date']
                area = axes.axvspan(start_date, end_date, color='red', alpha=0.5)
                frame.graph.figure_modifiers['lockdowns'].append(area)
        elif action == Constants.TOGGLE_INACTIVE:
            for area in frame.graph.figure_modifiers['lockdowns']:
                area.remove()
        else:
            raise InvalidParameterException(f'Unsupported action type {action}')

        frame.graph.canvas.draw()


if __name__ == '__main__':
    figure_provider = FigureProvider()
    all_figures = figure_provider.get_all_figures()

    gui = GuiController(all_figures)
    gui.mainloop()
