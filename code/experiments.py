import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from classes.rooster import *
from algorithms.evaluation import *
from algorithms.hillclimber import *
from algorithms.initialize import *

courses_df = pd.read_csv('../data/vakken.csv')
student_df = pd.read_csv('../data/studenten_en_vakken.csv')
rooms_df = pd.read_csv('../data/zalen.csv')
evenings = {'C0.110'}


def make_plot(nr_runs=20, type_rooster='random', algorithm='hc_activities', separated=False, rep=1):
    '''
    Accepts five optional arguments:
    · nr_runs = integer; tells how often the experiment should be conducted
    · type_rooster = 'random', 'greedy', 'large to small'
    · hc_activities = 'hc_activities', 'hc_students', 'hc_activities_and_students';
      tells which hillclimber should be used
    · separated = boolean; tells if the malus counts are shown separately or as their sum
    · rep = integer; tells how often the Hillclimber should be repeated for one experiment

    Keeps track of malus count per iteration for each run and creates a lineplot
    of the average, minimum and maximum malus count per iteration.
    '''
    if separated == False:
        # Create lists to track the total malus count
        malus_lists = []
        avg_maluses = []
        min_maluses = []
        max_maluses = []
    else:
        # Create lists to track the four different malus counts
        malus_lists_0 = []
        avg_maluses_0 = []
        min_maluses_0 = []
        max_maluses_0 = []

        malus_lists_1 = []
        avg_maluses_1 = []
        min_maluses_1 = []
        max_maluses_1 = []

        malus_lists_2 = []
        avg_maluses_2 = []
        min_maluses_2 = []
        max_maluses_2 = []

        malus_lists_3 = []
        avg_maluses_3 = []
        min_maluses_3 = []
        max_maluses_3 = []

    # Conduct experiment nr_runs times
    for i in range(nr_runs):
        my_rooster = Rooster(courses_df, student_df, rooms_df, evenings)
        my_rooster = Initialize(my_rooster)
        # Create starting rooster
        if type_rooster == 'random':
            my_rooster.make_rooster_random(4, 5, 7)
        elif type_rooster == 'greedy':
            my_rooster.make_rooster_greedy()
        else:
            my_rooster.make_rooster_largetosmall()

        my_rooster = Hillclimber(my_rooster)
        for i in range(rep):
            # Perform chosen Hillclimber
            if algorithm == 'hc_activities':
                my_rooster.hc_activities()
            elif algorithm == 'hc_students':
                my_rooster.hc_students('T')
                my_rooster.hc_students('P')
            else:
                my_rooster.hc_activities()
                my_rooster.hc_students('T')
                my_rooster.hc_students('P')

        # Append malus data from experiment to the correct list(s)
        if separated == False:
            malus_lists.append(my_rooster.maluses)
        else:
            malus_lists_0.append([item[0] for item in my_rooster.separated_maluses])
            malus_lists_1.append([item[1] for item in my_rooster.separated_maluses])
            malus_lists_2.append([item[2] for item in my_rooster.separated_maluses])
            malus_lists_3.append([item[3] for item in my_rooster.separated_maluses])

    # Create and plot lists of average, minimum and maximum maluses for each iteration
    if separated == False:
        for j in range(len(malus_lists[0])):
            combine_numbers = [item[j] for item in malus_lists]
            avg_maluses.append(np.mean(combine_numbers))
            min_maluses.append(np.min(combine_numbers))
            max_maluses.append(np.max(combine_numbers))

        plt.fill_between(x=np.linspace(1, len(malus_lists[0]), num=len(malus_lists[0])), y1=min_maluses, y2=max_maluses, alpha=0.4)
        plt.plot(np.linspace(1, len(malus_lists[0]), num=len(malus_lists[0])), avg_maluses)
    else:
        for j in range(len(malus_lists_0[0])):
            combine_numbers_0 = [item[j] for item in malus_lists_0]
            avg_maluses_0.append(np.mean(combine_numbers_0))
            min_maluses_0.append(np.min(combine_numbers_0))
            max_maluses_0.append(np.max(combine_numbers_0))

            combine_numbers_1 = [item[j] for item in malus_lists_1]
            avg_maluses_1.append(np.mean(combine_numbers_1))
            min_maluses_1.append(np.min(combine_numbers_1))
            max_maluses_1.append(np.max(combine_numbers_1))

            combine_numbers_2 = [item[j] for item in malus_lists_2]
            avg_maluses_2.append(np.mean(combine_numbers_2))
            min_maluses_2.append(np.min(combine_numbers_2))
            max_maluses_2.append(np.max(combine_numbers_2))

            combine_numbers_3 = [item[j] for item in malus_lists_3]
            avg_maluses_3.append(np.mean(combine_numbers_3))
            min_maluses_3.append(np.min(combine_numbers_3))
            max_maluses_3.append(np.max(combine_numbers_3))

        plt.fill_between(x=np.linspace(1, len(malus_lists_0[0]), num=len(malus_lists_0[0])), y1=min_maluses_0, y2=max_maluses_0, alpha=0.4)
        plt.plot(np.linspace(1, len(malus_lists_0[0]), num=len(malus_lists_0[0])), avg_maluses_0, label='overlap activiteiten')

        plt.fill_between(x=np.linspace(1, len(malus_lists_0[0]), num=len(malus_lists_0[0])), y1=min_maluses_1, y2=max_maluses_1, alpha=0.4)
        plt.plot(np.linspace(1, len(malus_lists_0[0]), num=len(malus_lists_0[0])), avg_maluses_1, label='tussenuren')

        plt.fill_between(x=np.linspace(1, len(malus_lists_0[0]), num=len(malus_lists_0[0])), y1=min_maluses_2, y2=max_maluses_2, alpha=0.4)
        plt.plot(np.linspace(1, len(malus_lists_0[0]), num=len(malus_lists_0[0])), avg_maluses_2, label='avondsloten')

        plt.fill_between(x=np.linspace(1, len(malus_lists_0[0]), num=len(malus_lists_0[0])), y1=min_maluses_3, y2=max_maluses_3, alpha=0.4)
        plt.plot(np.linspace(1, len(malus_lists_0[0]), len(malus_lists_0[0])), avg_maluses_3, label='capaciteit')

        plt.legend()

    plt.title(f'Gemiddeld aantal minpunten Hillclimbers (n={nr_runs}) met {type_rooster} beginrooster')
    plt.xlabel('Iteraties')
    plt.ylabel('Aantal minpunten')
    plt.show()


def make_histogram(nr_runs=500, type_rooster='random'):
    '''
    Accepts two optional arguments:
    · nr_runs = integer; tells how often the experiment should be conducted
    · type_rooster = 'random', 'greedy'

    Creates nr_runs times a greedy or random rooster and plots the
    corresponding maluspoints in a histogram.
    '''
    maluses = []
    for i in range(nr_runs):
        my_rooster = Rooster(courses_df, student_df, rooms_df, evenings)
        my_rooster = Initialize(my_rooster)

        # Perform the correct experiment
        if type_rooster == 'random':
            my_rooster.make_rooster_random(4, 5, 7)
        else:
            my_rooster.make_rooster_greedy()

        malus = sum(Evaluation(my_rooster).malus_count())
        maluses.append(malus)

    sns.histplot(x=maluses, kde=True)
    plt.title(f'Verdeling minpunten van {nr_runs} {type_rooster} roosters')
    plt.xlabel('Minpunten')
    plt.ylabel('Aantal')
    plt.show()


# Run the experiments
make_plot(nr_runs=3, type_rooster='random', separated=True, algorithm='hc_activities', rep=1)
make_histogram(100, 'random')
