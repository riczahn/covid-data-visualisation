import datetime

import matplotlib.pyplot as plt
import pandas as pd

from Formatter import Formatter


class FigureProvider:
    def __init__(self):
        self.formatter = Formatter()

    def get_uk_overall_deaths(self, figure_size):
        df = pd.read_csv('data/uk/deaths_registered_summary_statistics.csv').iloc[:, :-1]
        df = df.set_index('Week number').T

        data_2021 = {}
        data_2020 = {}

        # transform data into a more usable format, where the week number is transformed
        # to the date of that weeks monday
        for index, row in df.iterrows():
            week_as_date_2021 = datetime.datetime.strptime('2021-W' + index.strip() + '-1', "%Y-W%W-%w").strftime(
                "%Y-%m-%d")
            data_2021[week_as_date_2021] = row['Total deaths, all ages (2021)']

            week_as_date_2020 = datetime.datetime.strptime('2020-W' + index.strip() + '-1', "%Y-W%W-%w").strftime(
                "%Y-%m-%d")
            data_2020[week_as_date_2020] = row['Total deaths, all ages (2020)']

        data_of_both_years = {**data_2020, **data_2021}
        cool_df = pd.DataFrame.from_dict(data_of_both_years, orient='index', columns=['Weekly Deaths'])

        # parse values to float
        cool_df = cool_df.apply(lambda x: x.str.replace(',', '').astype(float), axis=1)

        figure = plt.Figure(figsize=figure_size, dpi=100)
        axis = figure.add_subplot(111)
        cool_df.plot(use_index=True, ax=axis, kind='bar')
        # todo maybe also plot the part of covid deaths? So that we can see the impact of covid? Or in a different graph

        return figure

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
        df = pd.read_excel('data/uk/Weekly_Influenza_and_COVID19_report_data_w27v2_2021.xlsx',
                           sheet_name='Figure 45. SARIWatch-ICUagegrp', header=8, nrows=53)
        df = df.drop(columns='Unnamed: 0')
        df = df.rename(columns={'Unnamed: 1': 'Week'})

        df['total'] = df.loc[:, '0 to 4':].sum(axis=1)

        for c in df.columns[1:-1]:
            df[c] = df[c] / df['total']

        figure = plt.Figure(figsize=figure_size, dpi=100)
        axis = figure.add_subplot(111)

        df.plot(x=df.columns[0], y=df.columns[1:-1], kind='bar', figsize=figure_size, stacked=True, ax=axis)
        axis.set_title('Weekly Covid Deaths by Age Group')

        # CHECK if is this data normalised to per 100.000 inhabitants?

        return figure

    def get_uk_daily_deaths(self, figure_size):
        df = pd.read_csv('data/uk/new_covid_deaths_daily_28_days_definition.csv', parse_dates=['date'])

        figure = plt.Figure(figsize=figure_size, dpi=100)
        axis = figure.add_subplot(111)
        df.plot(x='date', y='newDeaths28DaysByDeathDate', ax=axis)
        axis.set_title('Daily Covid Deaths in the UK')
        return figure

    def get_uk_pre_conditions_for_covid_deaths(self, figure_size):
        df = pd.read_excel('data/uk/deathsduetocovid19preexisitingconditions.xlsx', sheet_name='1', header=4)
        df = df.iloc[1:, :]  # drop first row since its all deaths accumulated

        figure = plt.Figure(figsize=figure_size, dpi=100)
        figure.subplots_adjust(left=0.53)
        axis = figure.add_subplot(111)
        df.plot(x='Pre-exisiting condition of death due to COVID-19',
                y=['Aged 0 to 64 years \n(Number of deaths)', 'Aged 65 years and over\n(Number of deaths)'], ax=axis,
                kind='barh')
        axis.set_title('Most common pre-conditions of COVID-19-Deaths')

        return figure

    def get_uk_number_of_pre_conditions_for_covid_deaths(self, figure_size):
        df = pd.read_excel('data/uk/deathsduetocovid19preexisitingconditions.xlsx', sheet_name='2', header=3)
        df = df[df.Unit != 'Average number of pre-exisiting conditions of COVID-19 deaths']
        df = df[df.Unit != 'Proportion of COVID-19 deaths with no pre-exisiting conditions']

        figure = plt.Figure(figsize=figure_size, dpi=100)
        figure.subplots_adjust(bottom=0.2)
        axis = figure.add_subplot(111)

        # Transpose table and drop last row
        df = df.set_index('Unit').T
        df = df[:-1]
        # normalise
        df = df.div(df.sum(axis=1), axis=0)

        df.plot(use_index=True, y=df.columns, kind='bar', stacked=True, ax=axis)

        return figure

    def get_all_figures(self, figure_size):
        return {
            'Tests and Cases': self.get_uk_covid_tests_and_cases(figure_size),
            'Overall Deaths 2020-2021': self.get_uk_overall_deaths(figure_size),
            'Daily Deaths': self.get_uk_daily_deaths(figure_size),
            'Weekly Deaths by Age Group': self.get_uk_deaths_by_week(figure_size),
            'Pre-Conditions': self.get_uk_pre_conditions_for_covid_deaths(figure_size),
            'Number of Pre-Conditions': self.get_uk_number_of_pre_conditions_for_covid_deaths(figure_size)
        }
