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


def format_number(data_value, index):
    """
    Formats the number below one million to use K for thousands (e.g. 700K) and above to use M for millions (e.g. 1M).
    """
    if data_value >= 1_000_000:
        formatter = '{:1.1f}M'.format(data_value * 0.000_001)
    else:
        formatter = '{:1.0f}K'.format(data_value * 0.001)
    return formatter


def plot_death_cases_history():
    data = load_population_development()
    plot = data.plot(x='Jahr', y='Sterbefälle', title="Death Cases in Germany 1950 - 2020", ylabel="Deaths",
                       xlabel="Year", yticks=[700_000, 800_000, 900_000, 1_000_000], legend=False, style="black", rot=0)

    plot.yaxis.set_major_formatter(format_number)
    plt.show()


if __name__ == '__main__':
    plot_death_cases_history()
