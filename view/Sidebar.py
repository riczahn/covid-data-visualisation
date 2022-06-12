import tkinter as tk
from tkinter import ttk

import Constants


class Sidebar(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.buttons = {}

        available_graphs = controller.get_all_graphs()
        self.combo_box = ttk.Combobox(self, values=available_graphs, state='readonly')
        self.combo_box.set(controller.get_current_graph())
        self.combo_box.bind("<<ComboboxSelected>>", self.handle_change)
        self.combo_box.pack(side=tk.TOP, anchor=tk.W, fill=tk.BOTH)

        self.buttons['lockdowns'] = {
            'button': tk.Button(master=self, text="Show Lockdowns", command=lambda: self.button_callback('lockdowns'),
                                relief="raised"),
            'active': False,
            'callback': controller.show_lockdowns
        }

        self.buttons['covid_events'] = {
            'button': tk.Button(master=self, text="Show Covid Events",
                                command=lambda: self.button_callback('covid_events'), relief="raised"),
            'active': False,
            'callback': controller.show_covid_events
        }

        for button_details in self.buttons.values():
            button = button_details['button']
            button.pack(side=tk.TOP, anchor=tk.W, fill=tk.BOTH)

    def button_callback(self, button_ref):
        button_details = self.buttons.get(button_ref)

        if button_details['active']:
            button_details['active'] = False
            button_details['button'].config(relief='raised')
            button_details['callback'](Constants.TOGGLE_INACTIVE)
        else:
            button_details['active'] = True
            button_details['button'].config(relief='sunken')
            button_details['callback'](Constants.TOGGLE_ACTIVE)

    def handle_change(self, event):
        self.controller.show_frame(self.combo_box.get())
