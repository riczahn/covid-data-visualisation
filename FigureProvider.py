import datetime

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

from Formatter import Formatter


class FigureProvider:
    def __init__(self):
        self.formatter = Formatter()

    def get_uk_overall_deaths(self, figure_size):
        overall_deaths = pd.read_csv('data/uk/deaths_registered_summary_statistics.csv').iloc[:, :-1]
        overall_deaths = overall_deaths.set_index('Week number').T

        data_2021 = {}
        data_2020 = {}

        # transform data into a more usable format, where the week number is transformed
        # to the date of that weeks monday
        for index, row in overall_deaths.iterrows():
            week_as_date_2021 = datetime.datetime.strptime('2021-W' + index.strip() + '-1', "%Y-W%W-%w").strftime(
                "%Y-%m-%d")
            data_2021[week_as_date_2021] = row['Total deaths, all ages (2021)']

            week_as_date_2020 = datetime.datetime.strptime('2020-W' + index.strip() + '-1', "%Y-W%W-%w").strftime(
                "%Y-%m-%d")
            data_2020[week_as_date_2020] = row['Total deaths, all ages (2020)']

        data_of_both_years = {**data_2020, **data_2021}

        period_index = pd.PeriodIndex(data=data_of_both_years.keys(), freq='W')
        plottable_df = pd.DataFrame(data=data_of_both_years.values(), index=period_index, columns=['Overall Deaths'])

        # parse values to float
        plottable_df = plottable_df.apply(lambda x: x.str.replace(',', '').astype(float), axis=1)

        covid_deaths = pd.read_csv('data/uk/weekly_covid_deaths.csv')

        # remove all nations besides England and Wales and order by date ascending
        covid_deaths_england = covid_deaths[covid_deaths.areaName == 'England'].iloc[::-1]
        covid_deaths_wales = covid_deaths[covid_deaths.areaName == 'Wales'].iloc[::-1]

        # drop all rows regarding 2022
        covid_deaths_england = covid_deaths_england[~covid_deaths_england['date'].astype(str).str.startswith('2022-')]
        covid_deaths_wales = covid_deaths_wales[~covid_deaths_wales['date'].astype(str).str.startswith('2022-')]

        # create period index with week frequency
        covid_period_index = pd.PeriodIndex(data=covid_deaths_england['date'], freq='W')
        covid_deaths_england.index = covid_period_index
        covid_deaths_wales.index = covid_period_index

        # drop all columns except the deaths, but rename those after the nation
        covid_deaths_england = covid_deaths_england.drop(columns=['date', 'areaCode', 'areaType', 'areaName']).rename(
            columns={'newWeeklyNsoDeathsByRegDate': 'England'})
        covid_deaths_wales = covid_deaths_wales.drop(columns=['date', 'areaCode', 'areaType', 'areaName']).rename(
            columns={'newWeeklyNsoDeathsByRegDate': 'Wales'})

        all_covid_deaths = pd.concat([covid_deaths_england.reset_index(), covid_deaths_wales.reset_index()], axis=1)

        # drop first column (duplicated date column) and set index back to date
        all_covid_deaths = all_covid_deaths.iloc[:, 1:].set_index('date')

        all_data = plottable_df.join(all_covid_deaths, how='left').fillna(0)
        all_data['Covid Deaths'] = all_data['England'] + all_data['Wales']
        all_data['Non-Covid Deaths'] = all_data['Overall Deaths'] - all_data['Covid Deaths']

        figure = plt.Figure(figsize=figure_size, dpi=100)
        axis = figure.add_subplot(111)
        all_data.plot(y=['Non-Covid Deaths', 'Covid Deaths'], kind='bar', stacked=True, color=['gray', 'red'], ax=axis)

        figure.autofmt_xdate()

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

    def get_uk_cases_by_week(self, figure_size):
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

    def get_uk_weekly_deaths_per_age_group(self, figure_size):
        data = pd.read_excel('data/uk/Weekly_covid_deaths.xlsx', sheet_name='Dataset', header=2)
        data = data.drop(columns=['Geography', 'Geography code', 'Sex', 'Deaths'])

        weekly_deaths_by_age_group = pd.DataFrame(
            columns=['Week', '0-1', '1-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44',
                     '45-49',
                     '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85-89', '90+'])

        rows = []
        current_week = None
        current_row_2020 = {}
        current_row_2021 = {}
        current_row_2022 = {}
        for index, row in data.iterrows():
            if current_week != row['Week']:
                # save old week to dict
                if current_row_2020 != {} and '1-4' in current_row_2020:
                    rows.append(current_row_2020)

                if current_row_2021 != {} and '1-4' in current_row_2021:
                    rows.append(current_row_2021)

                if current_row_2022 != {} and '1-4' in current_row_2022:
                    rows.append(current_row_2022)

                # reset rows
                current_row_2020 = {}
                current_row_2021 = {}
                current_row_2022 = {}

                # transform week number to date
                current_week = row['Week']
                week_number = row['Week'][(len('Week ')):]
                week_as_date_2020 = datetime.datetime.strptime('2020-W' + week_number.strip() + '-1',
                                                               "%Y-W%W-%w").strftime("%Y-%m-%d")
                current_row_2020['Week'] = week_as_date_2020

                week_as_date_2021 = datetime.datetime.strptime('2021-W' + week_number.strip() + '-1',
                                                               "%Y-W%W-%w").strftime("%Y-%m-%d")
                current_row_2021['Week'] = week_as_date_2021

                week_as_date_2022 = datetime.datetime.strptime('2022-W' + week_number.strip() + '-1',
                                                               "%Y-W%W-%w").strftime("%Y-%m-%d")
                current_row_2022['Week'] = week_as_date_2022

            # only add rows that are not nan
            if not np.isnan(row['2020']):
                current_row_2020[row['AgeGroups']] = row['2020']
            if not np.isnan(row['2021']):
                current_row_2021[row['AgeGroups']] = row['2021']
            if not np.isnan(row['2022']):
                current_row_2022[row['AgeGroups']] = row['2022']

        weekly_deaths_by_age_group = weekly_deaths_by_age_group.append(rows)

        # create index
        period_index = pd.PeriodIndex(data=weekly_deaths_by_age_group['Week'], freq='W')
        weekly_deaths_by_age_group = weekly_deaths_by_age_group.set_index(period_index).drop(columns=['Week'])

        # drop all rows with only zeros
        rows_with_only_0 = []
        for index, row in weekly_deaths_by_age_group.iterrows():
            if row.sum() == 0.0:
                rows_with_only_0.append(index)

        weekly_deaths_by_age_group = weekly_deaths_by_age_group.drop(index=rows_with_only_0)

        # combine age groups
        weekly_deaths_by_age_group['0-14'] = weekly_deaths_by_age_group['0-1'] + weekly_deaths_by_age_group['1-4'] + \
                                             weekly_deaths_by_age_group['5-9'] + weekly_deaths_by_age_group['10-14']

        weekly_deaths_by_age_group['15-34'] = weekly_deaths_by_age_group['15-19'] + weekly_deaths_by_age_group[
            '20-24'] + weekly_deaths_by_age_group['25-29'] + weekly_deaths_by_age_group['30-34']

        weekly_deaths_by_age_group = weekly_deaths_by_age_group.drop(
            columns=['0-1', '1-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34'])

        # move the new columns to the left
        cols = weekly_deaths_by_age_group.columns.tolist()
        cols = cols[-2:] + cols[:-2]

        weekly_deaths_by_age_group = weekly_deaths_by_age_group[cols]

        # normalise
        weekly_deaths_by_age_group = weekly_deaths_by_age_group.div(weekly_deaths_by_age_group.sum(axis=1), axis=0)

        # sort
        weekly_deaths_by_age_group.sort_index(inplace=True)
        weekly_deaths_by_age_group.index = weekly_deaths_by_age_group.index.weekofyear

        figure = plt.Figure(figsize=figure_size, dpi=100)
        axis = figure.add_subplot(111)
        figure.subplots_adjust(bottom=0.2)
        weekly_deaths_by_age_group.plot(kind='bar', stacked=True, ax=axis)

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

    def get_uk_yearly_deaths(self, figure_size):
        original_data = pd.read_excel('data/uk/yearly_deaths.xls', sheet_name='Table', header=14)[1:]
        # invert to make 2019 be the last row
        original_data = original_data.iloc[::-1]

        period_index = pd.PeriodIndex(data=original_data['Year'], freq='A')
        original_data.index = period_index

        # drop all columns besides the absolute death numbers
        original_data = original_data.iloc[:, 1:2]

        # create an ARIMA model and make a 5 year forecast
        model = ARIMA(original_data, order=(5, 1, 10))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=5)

        figure = plt.Figure(figsize=figure_size, dpi=100)
        figure.subplots_adjust(bottom=0.2)
        ax = figure.add_subplot(111)

        original_data.plot(ax=ax, color='black')
        forecast.plot(ax=ax, color='r', legend=True, label='Prediction')

        return figure

    def get_leading_causes_of_death(self, figure_size):
        df = pd.read_excel('data/uk/mortality_analysis_2013_to_2020.xlsx', sheet_name='Data', header=9, skipfooter=3,
                           index_col=0)

        # add a column for the values of 2020 without COVID-19
        df['2020 - w/o COVID-19'] = df[2020]
        df.at['LC47 COVID-19', '2020 - w/o COVID-19'] = 0

        for column in df.columns:
            df[column] = df[column] / df[column].sum(axis=0)

        figure = plt.Figure(figsize=figure_size, dpi=100)
        figure.subplots_adjust(bottom=0.25)
        ax = figure.add_subplot(111)

        df.T.plot(kind='bar', stacked=True, ax=ax, legend=False)

        figure.autofmt_xdate()

        return figure

    def get_all_figures(self, figure_size):
        return {
            'Tests and Cases': self.get_uk_covid_tests_and_cases(figure_size),
            'Yearly Deaths 1830 - 2024': self.get_uk_yearly_deaths(figure_size),
            'Overall Deaths 2020-2021': self.get_uk_overall_deaths(figure_size),
            'Daily Deaths': self.get_uk_daily_deaths(figure_size),
            'Weekly Cases by Age Group': self.get_uk_cases_by_week(figure_size),
            'Weekly Deaths by Age Group': self.get_uk_weekly_deaths_per_age_group(figure_size),
            'Leading Causes of Death': self.get_leading_causes_of_death(figure_size),
            'Pre-Conditions': self.get_uk_pre_conditions_for_covid_deaths(figure_size),
            'Number of Pre-Conditions': self.get_uk_number_of_pre_conditions_for_covid_deaths(figure_size)
        }
