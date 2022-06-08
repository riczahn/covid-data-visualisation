import matplotlib.pyplot as plt
import pandas as pd

from Formatter import Formatter


class FigureProvider:
    def __init__(self):
        self.formatter = Formatter()

    def get_uk_covid_tests_and_cases(self):
        data = pd.read_csv('data/uk/UK_new_cases_and_tests.csv', parse_dates=['date'])

        figure = plt.Figure(figsize=(6, 5), dpi=100)
        axis = figure.add_subplot(111)
        plot = data.plot(x='date', y=['newVirusTestsByPublishDate', 'newCasesBySpecimenDate'], color=['b', 'r'], ax=axis)
        plot.yaxis.set_major_formatter(self.formatter.format_numbers)
        plot.xaxis.set_major_formatter(self.formatter.format_dates())
        axis.set_title('New Covid Cases & Tests')
        figure.autofmt_xdate()
        return figure

    def get_de_death_cases_history(self):
        data = pd.read_csv('data/population_development.csv', delimiter=';')

        figure = plt.Figure(figsize=(6, 5), dpi=100)
        axis = figure.add_subplot(111)
        plot = data.plot(x='Jahr', y='Sterbefälle', title="Death Cases in Germany 1950 - 2020", ylabel="Deaths",
                         xlabel="Year", yticks=[700_000, 800_000, 900_000, 1_000_000], legend=False, style="black",
                         rot=0, ax=axis)

        plot.yaxis.set_major_formatter(self.formatter.format_numbers)
        axis.set_title('Death Cases in Germany 1950 - 2020')
        return figure

    def get_all_figures(self):
        return {
            'uk': self.get_uk_covid_tests_and_cases(),
            'de': self.get_de_death_cases_history()
        }
