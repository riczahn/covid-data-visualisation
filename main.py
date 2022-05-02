import pandas as pd


def func():
    dataframe = pd.read_csv('data/death_cases/Monthly_Deaths_Per_Age_Group_Women_2016-2022.csv')
    print(dataframe)


if __name__ == '__main__':
    func()

