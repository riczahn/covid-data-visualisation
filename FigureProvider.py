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

    def get_uk_deaths_by_week(self, figure_size):
        death_by_week_2021_df = pd.read_csv('data/uk/UK_Weekly_deaths.csv')

        figure = plt.Figure(figsize=figure_size, dpi=100)
        axis = figure.add_subplot(111)
        plot = death_by_week_2021_df.plot(x='Week of death',
                                          y=['28 day definition', '60 day definition'], kind='bar', ax=axis)
        plot.yaxis.set_major_formatter(self.formatter.format_numbers)
        axis.set_title('Covid Death Cases in the UK')
        return figure

    def get_uk_daily_deaths(self, figure_size):
        df = pd.read_csv('data/uk/new_covid_deaths_daily_28_days_definition.csv', parse_dates=['date'])

        figure = plt.Figure(figsize=figure_size, dpi=100)
        axis = figure.add_subplot(111)
        df.plot(x='date', y='newDeaths28DaysByDeathDate', ax=axis)
        axis.set_title('Daily Covid Deaths in the UK')
        return figure

    def get_uk_daily_deaths_by_age_group(self, figure_size):
        df = pd.read_csv('data/uk/age_group_daily_covid_deaths.csv', parse_dates=['date'])

        figure = plt.Figure(figsize=figure_size, dpi=100)
        axis = figure.add_subplot(111)
        df.plot(x='date', y='deaths', stacked=True, ax=axis)  # todo: How to plot this 3 dimensional data?
        axis.set_title('Daily Covid Deaths by age group')
        return figure

    def get_uk_pre_conditions_for_covid_deaths(self, figure_size):
        df = pd.read_excel('data/uk/deathsduetocovid19preexisitingconditions.xlsx', sheet_name='1', header=4)
        df = df.iloc[1:, :]  # drop first row since its all deaths accumulated

        figure = plt.Figure(figsize=figure_size, dpi=100)
        sub_figures = figure.subfigures(1, 2, wspace=0.07)

        left_axis = sub_figures[0].subplots(1, 1)
        df.plot.pie(y='Aged 0 to 64 years \n(Proportion of deaths)', labels=None, autopct='%.1f%%', ax=left_axis,
                    legend=False)
        left_axis.set_title('Pre-Conditions of COVID-19 deaths with age 0-64')
        left_axis.get_yaxis().set_visible(False)

        right_axis = sub_figures[1].subplots(1, 1)
        df.plot.pie(y='Aged 65 years and over\n(Proportion of deaths)', labels=None, autopct='%.1f%%', ax=right_axis,
                    legend=False)
        right_axis.set_title('Pre-Conditions of COVID-19 deaths with age 65+')
        right_axis.get_yaxis().set_visible(False)

        # todo somehow the values are not correct. biggest part for age 0-64 should be 29.1%

        return figure

    def get_all_figures(self, figure_size):
        return {
            'Tests and Cases': self.get_uk_covid_tests_and_cases(figure_size),
            'Daily Deaths': self.get_uk_daily_deaths(figure_size),
            'Weekly Deaths': self.get_uk_deaths_by_week(figure_size),
            'Deaths by Age Group': self.get_uk_daily_deaths_by_age_group(figure_size),
            'Pre-Conditions': self.get_uk_pre_conditions_for_covid_deaths(figure_size)
        }
