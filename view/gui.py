import tkinter

from view.Graph import Graph

root = tkinter.Tk()
root.wm_title("Embedding in Tk")

graph = Graph(root)
graph.draw()


def _quit():
    root.quit()
    root.destroy()


button = tkinter.Button(master=root, text="Quit", command=_quit)
button.pack(side=tkinter.BOTTOM)

tkinter.mainloop()

if __name__ == '__main__':
    pass
