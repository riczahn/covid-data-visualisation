import pandas as pd
import numpy
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler


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


def placeholder_uk():
    x = [1, 2, 3, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 18, 19, 21, 22]
    y = [100, 90, 80, 60, 60, 55, 60, 65, 70, 70, 75, 76, 78, 79, 90, 99, 99, 100]

    df = pd.read_csv('data/uk/UK_data_v1.csv')

    date = df['date']
    new_cases = df['newCasesBySpecimenDate']

    print(date)
    print(new_cases)

    my_model = numpy.poly1d(numpy.polyfit(x, y, 3))
    my_line = numpy.linspace(1, len(date), 100)
    df.plot(x='date', y='newCasesBySpecimenDate')


def show_graph_v1():
    root = tk.Tk()
    bar1 = FigureCanvasTkAgg(build_graph(), root)
    bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    root.mainloop()


def show_graph_v2():
    # will print an interactive window when executed via cmd
    plot = df.plot(x='date', y=['newVirusTestsByPublishDate', 'newCasesBySpecimenDate'], color=['b', 'r'])
    plot.yaxis.set_major_formatter(format_number)
    plt.show()


def build_graph():
    df = pd.read_csv('data/uk/UK_new_cases_and_tests.csv')

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
