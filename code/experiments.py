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

def experiment(initial_T=50, nr_runs=10, type_rooster='random'):
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

experiment()
