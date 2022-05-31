import tkinter as tk

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
    Formats numbers below one million to use K for thousands (e.g. 700K) and above to use M for millions (e.g. 1M).
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


def plot_monthly_death_cases():
    data = load_monthly_male_death_cases_per_age_group()
    print(data)
    data.drop(columns=["Nr.", "Jahr", "unter … Jahren", "Insgesamt"], inplace=True)

    print(data)
    rows = [i * 18 for i in range(int(data.size/18))]
    print(rows)


def build_graph():
    df = pd.read_csv('../data/uk/UK_new_cases_and_tests.csv')

    figure1 = plt.Figure(figsize=(6, 5), dpi=100)
    ax1 = figure1.add_subplot(111)
    plot = df.plot(x='date', y=['newVirusTestsByPublishDate', 'newCasesBySpecimenDate'], color=['b', 'r'], ax=ax1)
    plot.yaxis.set_major_formatter(format_number)
    ax1.set_title('New Covid Cases & Tests')
    return figure1


def build_ui():
    root = tk.Tk()
    bar1 = FigureCanvasTkAgg(build_graph(), root)
    bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    # if we want to add a small zoom thing
    # figure1.add_axes([0.2, 0.3, 0.2, 0.2])
    root.mainloop()


if __name__ == '__main__':
    # button = tk.Button(root, text='Show Graph', command=show_graph_v1)
    # button.pack()

    # show_graph_v1()
    # build_ui()
    pass
