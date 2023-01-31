import pandas as pd
from classes.rooster import *
from algorithms.evaluation import *
from algorithms.hillclimber import *
from algorithms.initialize import *
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math
import time
import pickle
import sys

courses_df = pd.read_csv('../data/vakken.csv')
student_df = pd.read_csv('../data/studenten_en_vakken2.csv')
rooms_df = pd.read_csv('../data/zalen.csv')
evenings = {'C0.110'}
sys.setrecursionlimit(5000)

class Simulated_Annealing():
    def __init__(self, lowest_rooster, initial_T, reheat_point,
     nr_runs = 500000, g = 0.998, final_T=0.0001):
        self.g = g
        self.nr_runs = nr_runs
        self.initial_T = initial_T
        self.current_T = initial_T
        self.final_T = final_T
        self.reheat_point = reheat_point
        self.i = 0
        self.rooms = lowest_rooster.rooms
        self.activities = lowest_rooster.activities
        self.courses = lowest_rooster.courses
        self.students = lowest_rooster.students
        self.lowest_rooster = lowest_rooster

    def geometric(self):
        '''
        Geometric cooling method
        '''
        self.current_T *= (self.g) ** self.i

    def linear(self, alpha=0.001):
        '''
        Linear cooling method
        '''
        self.current_T -= alpha

    def logarithmic(self):
        '''
        Logarithmic cooling method
        '''
        self.current_T = self.initial_T / (1 + math.log(1 + self.i))

    def exponential(self):
        '''
        Exponential cooling method
        '''
        self.current_T = max(0.05, self.current_T * self.g)

    def run(self):
        '''
        This function applies the simulated annealing algorithm,
        where it declines a lecture swap with a random
        chance > e ^ (delta / T). It cools down via one of the
        called cooling methods above. The lecture swap swaps two
        randomly chosen lectures. It saves the malus for each rooster
        and it returns the best rooster with best malus.
        '''
        dict = {}

        while self.i < self.nr_runs:

            # Random room and slot from activities
            lecture1 = random.choice(self.activities)
            room1 = lecture1.room
            slot1 = lecture1.slot

            # Room2 could also be an empty room
            slots = []
            room2 = random.choice(self.rooms)
            for slot in np.ndindex(room2.rooster.shape):
                slots.append(slot)
            slot2 = random.choice(slots)
            lecture2 = room2.rooster[slot2]

            # Malus before swap
            old = sum(Evaluation(self).malus_count())

            # Swapping lectures
            Hillclimber(self).swap_course(room1, lecture1, slot1, room2, lecture2, slot2)

            # Malus after swap
            new = sum(Evaluation(self).malus_count())

            # Decline swap with delta > 50 or random chance
            if new > old + 50 or random.uniform(0, 1) > round(math.exp((old-new) / self.current_T),10):
                Hillclimber(self).swap_course(room1, lecture2, slot1, room2, lecture1, slot2)

            # Apply cooling method
            self.exponential()

            print(sum(Evaluation(self).malus_count()), "\t", self.current_T)

            # Save rooster with corresponding malus
            dict[self.lowest_rooster] = sum(Evaluation(self).malus_count())
            self.i += 1
            #self.malus_list.append(sum(Evaluation(self).malus_count()))

            if self.i % self.reheat_point == 0:
                self.current_T += 5

        # Get rooster with lowest malus
        best_rooster = min(dict, key=dict.get)
        best_malus = min(dict.values())

        # Save rooster to file
        with open(f'SA_RoosterWith{min(dict.values())}Points_{self.nr_runs/self.reheat_point}reheats', 'wb') as outp:
            pickle.dump(best_rooster, outp, pickle.HIGHEST_PROTOCOL)

        return best_rooster, best_malus

# my_rooster = Rooster(courses_df, student_df, rooms_df, evenings)
# my_rooster = Initialize(my_rooster)

# def experiment(my_rooster, initial_T):
#     maluses = []
#     for i in range(2):
#         my_rooster.make_rooster_greedy()
#         results = Simulated_Annealing(my_rooster, initial_T).run()
    # my_rooster = Hillclimber(my_rooster)

    # for i in range(2):
    #     my_rooster.hc_activities()
    #     initial_T -= 2
    #     results = Simulated_Annealing(my_rooster, initial_T).run()
    #     plt.scatter(results[1], results[0])
    #     plt.show()

#experiment = experiment(my_rooster, 50)

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
    result = Simulated_Annealing(lowest_rooster, initial_T, 100000).run()
    sa_rooster = result[0]
    malus_list.append(result[1])
    stop = time.time()
    print(f'Runtime for simulated annealing is : {stop-start}')
    #print(j, malus_list)

    return malus_list

experiment()



# maluses = []
# for i in range(5000):
#     my_rooster = Rooster(courses_df, student_df, rooms_df, evenings)
#     my_rooster = Initialize(my_rooster)
#     my_rooster.make_rooster_random(4, 5, 7)
#     maluses.append(sum(Evaluation(my_rooster).malus_count()))
#
# std = np.std(maluses)
# print(std)
#
# sns.histplot(x=maluses, binwidth=20, kde=True)
# plt.show()
