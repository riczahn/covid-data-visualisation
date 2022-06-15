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
        figure.subplots_adjust(left=0.53)
        axis = figure.add_subplot(111)
        df.plot(x='Pre-exisiting condition of death due to COVID-19', y=['Aged 0 to 64 years \n(Number of deaths)', 'Aged 65 years and over\n(Number of deaths)'], ax=axis, kind='barh')
        axis.set_title('Most common pre-conditions of COVID-19-Deaths')

        return figure

    def get_uk_number_of_pre_conditions_for_covid_deaths(self, figure_size):
        df = pd.read_excel('data/uk/deathsduetocovid19preexisitingconditions.xlsx', sheet_name='2', header=3)
        df = df[df.Unit != 'Average number of pre-exisiting conditions of COVID-19 deaths']
        df = df[df.Unit != 'Proportion of COVID-19 deaths with no pre-exisiting conditions']

        figure = plt.Figure(figsize=figure_size, dpi=100)
        left_axis = figure.add_axes([0, 0.2, 0.5, 0.7], aspect=1)
        df.plot.pie(y='Aged 0 to 64 years ', labels=None, autopct='%.1f%%', pctdistance=1.2,
                    ax=left_axis,
                    legend=False, textprops={'fontsize': 8})
        left_axis.set_title('Number of pre-conditions age 0-64')
        left_axis.get_yaxis().set_visible(False)

        right_axis = figure.add_axes([0.5, 0.2, 0.5, 0.7], aspect=1)
        df.plot.pie(y='Aged 65 years and over', labels=None, autopct='%.1f%%', pctdistance=1.2,
                    ax=right_axis,
                    legend=False, textprops={'fontsize': 8})
        right_axis.set_title('Number of pre-conditions age 65+')
        right_axis.get_yaxis().set_visible(False)

        figure.legend(labels=df['Unit'], loc='lower center',
                      prop={'size': 8})

        return figure

    def get_all_figures(self, figure_size):
        return {
            'Tests and Cases': self.get_uk_covid_tests_and_cases(figure_size),
            'Daily Deaths': self.get_uk_daily_deaths(figure_size),
            'Weekly Deaths': self.get_uk_deaths_by_week(figure_size),
            'Deaths by Age Group': self.get_uk_daily_deaths_by_age_group(figure_size),
            'Pre-Conditions': self.get_uk_pre_conditions_for_covid_deaths(figure_size),
            'Number of Pre-Conditions': self.get_uk_number_of_pre_conditions_for_covid_deaths(figure_size)
        }
