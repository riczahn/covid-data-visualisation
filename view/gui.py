import tkinter as tk

from view.Graph import Graph

root = tk.Tk()
root.wm_title("Covid Analysis Tool")

graph = Graph(root)
graph.draw()


def _quit():
    root.quit()
    root.destroy()


button = tk.Button(master=root, text="Quit", command=_quit)
button.pack(side=tk.BOTTOM)

tk.mainloop()

if __name__ == '__main__':
    pass
