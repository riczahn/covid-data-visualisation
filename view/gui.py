import tkinter as tk

from FigureProvider import FigureProvider
from view.Graph import Graph
from view.Sidebar import Sidebar


def _quit():
    root.quit()
    root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.wm_title("Covid Analysis Tool")

    graph = Graph(root, FigureProvider())
    graph.pack()

    button = tk.Button(master=root, text="Quit", command=_quit)
    button.pack(side=tk.BOTTOM)

    sidebar = Sidebar(root, graph)
    sidebar.pack()

    tk.mainloop()
