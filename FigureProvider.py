import matplotlib.pyplot as plt
import pandas as pd

from Formatter import Formatter


class FigureProvider:
    def __init__(self):
        self.formatter = Formatter()

    def get_uk_covid_tests_and_cases(self, figure_size):
        data = pd.read_csv('data/uk/UK_new_cases_and_tests.csv', parse_dates=['date'])

        figure = plt.Figure(figsize=figure_size, dpi=100)
        axis = figure.add_subplot(111)
        plot = data.plot(x='date', y=['newVirusTestsByPublishDate', 'newCasesBySpecimenDate'], color=['b', 'r'],
                         ax=axis)
        plot.yaxis.set_major_formatter(self.formatter.format_numbers)
        plot.xaxis.set_major_formatter(self.formatter.format_dates())
        axis.set_title('New Covid Cases & Tests')
        figure.autofmt_xdate()
        return figure

    def get_de_death_cases_history(self, figure_size):
        data = pd.read_csv('data/population_development.csv', delimiter=';')

        figure = plt.Figure(figsize=figure_size, dpi=100)
        axis = figure.add_subplot(111)
        plot = data.plot(x='Jahr', y='Sterbefälle', title="Death Cases in Germany 1950 - 2020", ylabel="Deaths",
                         xlabel="Year", yticks=[700_000, 800_000, 900_000, 1_000_000], legend=False, style="black",
                         rot=0, ax=axis)

        plot.yaxis.set_major_formatter(self.formatter.format_numbers)
        axis.set_title('Death Cases in Germany 1950 - 2020')
        return figure

    def get_uk_deaths_by_week(self, figure_size):
        death_by_week_2021_df = pd.read_csv('data/uk/UK_Weekly_deaths.csv')

        figure = plt.Figure(figsize=figure_size, dpi=100)
        axis = figure.add_subplot(111)
        plot = death_by_week_2021_df.plot(x='Week of death',
                                          y=['28 day definition', '60 day definition'], kind='bar', ax=axis)
        plot.yaxis.set_major_formatter(self.formatter.format_numbers)
        axis.set_title('Covid Death Cases in the UK')
        return figure

    def get_all_figures(self, figure_size):
        return {
            'Tests and Cases': self.get_uk_covid_tests_and_cases(figure_size),
            'Deaths': self.get_uk_deaths_by_week(figure_size),
            'de': self.get_de_death_cases_history(figure_size)
        }
