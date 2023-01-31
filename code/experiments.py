import pandas as pd
import numpy as np
import math
import random
import numpy as np
import time
import pickle
import sys
import argparse
import yaml
import pdfschedule

from classes.rooster import Rooster
from student_rooster import rooster_per_student
from classes.rooster import *
from algorithms.evaluation import *
from algorithms.hillclimber import *
from algorithms.initialize import *
from algorithms.tabu_search import *
from algorithms.simulated_annealing import *


courses_df = pd.read_csv('../data/vakken.csv')
student_df = pd.read_csv('../data/studenten_en_vakken2.csv')
rooms_df = pd.read_csv('../data/zalen.csv')
evenings = {'C0.110'}
sys.setrecursionlimit(5000)

def SA_experiment(initial_T=50, nr_runs=10):
    '''
    Accepts an integer (nr_runs) and a string (type), which can be 'random' or
    'greedy'. Creates nr_runs times a greedy or random rooster and plots the
    corresponding maluspoints in a histogram.
    '''
    random_dict = {}
    reheat_list = [5000, 10000, 20000, 25000, 50000]
    malus_list = []
    for i in range(nr_runs):
        my_rooster = Rooster(courses_df, student_df, rooms_df, evenings)
        my_rooster = Initialize(my_rooster)
        my_rooster.make_rooster_greedy()
        malus = sum(Evaluation(my_rooster).malus_count())
        random_dict[my_rooster] = malus

    lowest_rooster = min(random_dict, key=random_dict.get)

    # for j in range(6):
    #     for heat in reheat_list:
    start = time.time()
    result = Simulated_Annealing(lowest_rooster, initial_T, 50000).run()
    sa_rooster = result[0]
    malus_list.append(result[1])
    stop = time.time()
    print(f'Runtime for simulated annealing is : {stop-start}')
    #print(j, malus_list)

    return malus_list

SA_experiment()


def make_plot(nr_runs=10, type_rooster='random', algorithm='hc_activities'):
    '''
    Accepts three optional arguments:
    · nr_runs = integer
    · type_rooster = 'random', 'greedy', 'large to small'
    · hc_activities = 'hc_activities', 'hc_students', 'hc_activities_and_students'
    Keeps track of malus count per iteration for each run and creates a lineplot
    of the average, minimum and maximum malus count per iteration.
    '''
    malus_lists = []
    avg_maluses = []
    min_maluses = []
    max_maluses = []

    for i in range(nr_runs):
        my_rooster = Rooster(courses_df, student_df, rooms_df, evenings)
        my_rooster = Initialize(my_rooster)

        if type_rooster == 'random':
            my_rooster.make_rooster_random(4, 5, 7)
        elif type_rooster == 'greedy':
            my_rooster.make_rooster_greedy()
        else:
            my_rooster.make_rooster_largetosmall()

        my_rooster = Hillclimber(my_rooster)

        if algorithm == 'hc_activities':
            my_rooster.hc_activities()
        elif algorithm == 'hc_students':
            my_rooster.hc_students('T')
            my_rooster.hc_students('P')
        else:
            my_rooster.hc_activities()
            my_rooster.hc_students('T')
            my_rooster.hc_students('P')

        malus_lists.append(my_rooster.maluses)

    # iterations = my_rooster.iterations

    for j in range(len(malus_lists[0])):
        combine_numbers = [item[j] for item in malus_lists]
        avg_maluses.append(np.mean(combine_numbers))
        min_maluses.append(np.min(combine_numbers))
        max_maluses.append(np.max(combine_numbers))

    plt.fill_between(x=np.linspace(1, 131, num=131), y1=min_maluses, y2=max_maluses, alpha=0.4)
    plt.plot(np.linspace(1, 131, num=131), avg_maluses)
    plt.title(f'Gemiddeld aantal minpunten Hillclimbers (n={nr_runs}) met {type_rooster} beginrooster')
    plt.xlabel('Iteraties')
    plt.ylabel('Aantal minpunten')
    plt.show()

make_plot(nr_runs=20, type_rooster='greedy')


def make_histogram(nr_runs=500, type_rooster='random'):
    '''
    Accepts an integer (nr_runs) and a string (type), which can be 'random' or
    'greedy'. Creates nr_runs times a greedy or random rooster and plots the
    corresponding maluspoints in a histogram.
    '''
    maluses = []
    for i in range(nr_runs):
        my_rooster = Rooster(courses_df, student_df, rooms_df, evenings)
        my_rooster = Initialize(my_rooster)

        if type_rooster == 'random':
            my_rooster.make_rooster_random(4, 5, 7)
        else:
            my_rooster.make_rooster_greedy()
        # print(i)
        malus = sum(Evaluation(my_rooster).malus_count())
        maluses.append(malus)

    print(maluses, min(maluses), max(maluses), np.mean(maluses), np.std(maluses))
    sns.histplot(x=maluses, kde=True)
    plt.title(f'Verdeling minpunten van {nr_runs} {type_rooster} roosters')
    plt.xlabel('Minpunten')
    plt.ylabel('Aantal')
    plt.show()

make_histogram(1000, 'greedy')
