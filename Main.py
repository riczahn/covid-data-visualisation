import Constants
from FigureProvider import FigureProvider
from view.Gui import GuiController

if __name__ == '__main__':
    figure_provider = FigureProvider()
    all_figures = figure_provider.get_all_figures(Constants.LARGE_FIGURE_SIZE)
    # Uncomment the following line if you want to use a smaller GUI
    # all_figures = figure_provider.get_all_figures(Constants.MEDIUM_FIGURE_SIZE)

    gui = GuiController(all_figures)
    gui.mainloop()
