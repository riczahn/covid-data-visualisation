import pandas as pd
import matplotlib.pyplot as plt

from Formatter import Formatter


class FigureProvider:
    def __init__(self):
        self.formatter = Formatter()

    def build_graph(self):
        df = pd.read_csv('data/uk/UK_new_cases_and_tests.csv')

        figure1 = plt.Figure(figsize=(6, 5), dpi=100)
        ax1 = figure1.add_subplot(111)
        plot = df.plot(x='date', y=['newVirusTestsByPublishDate', 'newCasesBySpecimenDate'], color=['b', 'r'], ax=ax1)
        plot.yaxis.set_major_formatter(self.formatter.format_numbers)
        ax1.set_title('New Covid Cases & Tests')
        return figure1
