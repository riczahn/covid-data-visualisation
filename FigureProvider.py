import pandas as pd
import matplotlib.pyplot as plt

from Formatter import Formatter


class FigureProvider:
    def __init__(self):
        self.formatter = Formatter()

    def get_uk_covid_tests_and_cases(self):
        df = pd.read_csv('data/uk/UK_new_cases_and_tests.csv', parse_dates=['date'])

        figure = plt.Figure(figsize=(6, 5), dpi=100)
        axis = figure.add_subplot(111)
        plot = df.plot(x='date', y=['newVirusTestsByPublishDate', 'newCasesBySpecimenDate'], color=['b', 'r'], ax=axis)
        plot.yaxis.set_major_formatter(self.formatter.format_numbers)
        plot.xaxis.set_major_formatter(self.formatter.format_dates())
        axis.set_title('New Covid Cases & Tests')
        figure.autofmt_xdate()
        return figure

    def get_de_death_cases_history(self):
        data = self.load_population_development()

        figure = plt.Figure(figsize=(6, 5), dpi=100)
        axis = figure.add_subplot(111)
        plot = data.plot(x='Jahr', y='Sterbefälle', title="Death Cases in Germany 1950 - 2020", ylabel="Deaths",
                         xlabel="Year", yticks=[700_000, 800_000, 900_000, 1_000_000], legend=False, style="black",
                         rot=0, ax=axis)

        plot.yaxis.set_major_formatter(self.formatter.format_numbers)
        axis.set_title('Death Cases in Germany 1950 - 2020')
        return figure

    def load_monthly_female_death_cases_per_age_group(self):
        return pd.read_csv('data/death_cases/Monthly_Deaths_Per_Age_Group_Women_2016-2022.csv')

    def load_monthly_male_death_cases_per_age_group(self):
        return pd.read_csv('data/death_cases/Monthly_Deaths_Per_Age_Group_Men_2016-2022.csv')

    def load_population_development(self):
        return pd.read_csv('data/population_development.csv', delimiter=';')

    def load_age_pyramid(self):
        return pd.read_csv('data/age_pyramid.csv', delimiter=';')
