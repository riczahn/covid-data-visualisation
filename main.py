import pandas as pd
import matplotlib.pyplot as plt


def load_monthly_female_death_cases_per_age_group():
    return pd.read_csv('data/death_cases/Monthly_Deaths_Per_Age_Group_Women_2016-2022.csv')


def load_monthly_male_death_cases_per_age_group():
    return pd.read_csv('data/death_cases/Monthly_Deaths_Per_Age_Group_Men_2016-2022.csv')


def load_population_development():
    return pd.read_csv('data/population_development.csv', delimiter=';')


def load_age_pyramid():
    return pd.read_csv('data/age_pyramid.csv', delimiter=';')


def main():
    population_development = load_population_development()
    deaths = population_development[['Jahr', 'Sterbefälle']]
    deaths.plot.bar(x='Jahr', y='Sterbefälle', rot=0)

    plt.show()


if __name__ == '__main__':
    main()

