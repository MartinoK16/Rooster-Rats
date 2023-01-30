import pandas as pd
from classes.rooster import *
from algorithms.evaluation import *
from algorithms.hillclimber import *
from algorithms.initialize import *
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math

courses_df = pd.read_csv('../data/vakken.csv')
student_df = pd.read_csv('../data/studenten_en_vakken2.csv')
rooms_df = pd.read_csv('../data/zalen.csv')
evenings = {'C0.110'}


# def simulated_annealing(self, alpha=0.05, initial_T=50):
#     final_T = 0.000001
#     current_T = initial_T
#     i = 0
#     value_count = 0
#
#     while current_T > final_T:
#         i += 1
#
#         # Loop over all the lectures randomly
#         for nr3, lecture1 in enumerate(random.sample(self.activities, len(self.activities))):
#             # Get the room and slot where this lecture is place now
#
#             room1 = lecture1.room
#             slot1 = lecture1.slot
#
#             # Loop over all the slots in each room
#             for nr2, room2 in enumerate(self.rooms):
#                 for slot2 in np.ndindex(room2.rooster.shape):
#
#
#                     # Get which lecture is placed in this room and slot
#                     # Swap these 2 lectures, get the new malus and put it in the dict and swap them back
#                     old = sum(Evaluation(self).malus_count())
#                     lecture2 = room2.rooster[slot2]
#                     self.swap_course(room1, lecture1, slot1, room2, lecture2, slot2)
#                     new = sum(Evaluation(self).malus_count())
#
#                     if new > old + 100:
#                         self.swap_course(room1, lecture2, slot1, room2, lecture1, slot2)
#
#                     elif random.uniform(0, 1) > 2 ** ((old - new) / current_T):
#                         self.swap_course(room1, lecture2, slot1, room2, lecture1, slot2)
#
#                     else:
#                         room1 = room2
#                         slot1 = slot2
#                         print('malus 1', Evaluation(self).malus_count())
#                         current_T *= 0.998 ** i
#                         #current_T -= 0.001
#                         #current_T = current_T / (1 + i * current_T)
#                         print(current_T)
#
#             # Get the updated malus count and print useful info
#             self.hillclimber_students('W')
#             self.hillclimber_students('P')
#             self.Evaluation(self).malus_count()()
#             print('malus 2', sum(self.malus))


class Simulated_Annealing():
    def __init__(self, lowest_rooster, initial_T, g = 0.998, final_T=0.0001):
        self.g = g
        self.initial_T = initial_T
        self.current_T = initial_T
        self.final_T = final_T
        self.i = 0
        self.rooms = lowest_rooster.rooms
        self.activities = lowest_rooster.activities
        self.courses = lowest_rooster.courses
        self.students = lowest_rooster.students
        self.lowest_rooster = lowest_rooster
        self.value_count = 0
        self.malus_list = []

    def geometric(self):
        self.current_T *= (self.g) ** self.i

    def linear(self, alpha=0.001):
        self.current_T -= alpha

    def logarithmic(self):
        self.current_T = self.initial_T / (1 + math.log(1 + self.i))

    def exponential(self):
        self.current_T = max(0.05, self.current_T * self.g)


    def run(self):
        dict = {}

        while self.i < 500000:

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

            old = sum(Evaluation(self).malus_count())
            Hillclimber(self).swap_course(room1, lecture1, slot1, room2, lecture2, slot2)
            new = sum(Evaluation(self).malus_count())

            if new > old + 50 or random.uniform(0, 1) > round(math.exp((old-new) / self.current_T),10):
                Hillclimber(self).swap_course(room1, lecture2, slot1, room2, lecture1, slot2)

            self.exponential()

            print(sum(Evaluation(self).malus_count()), "\t", self.current_T)

            dict[self.lowest_rooster] = sum(Evaluation(self).malus_count())
            self.i += 1
            #self.malus_list.append(sum(Evaluation(self).malus_count()))

            if self.i % 50000 == 0:
                self.current_T += 5

            best_rooster = min(dict, key=dict.get)


        return best_rooster

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

def experiment(initial_T, nr_runs=100, type_rooster='random'):
    '''
    Accepts an integer (nr_runs) and a string (type), which can be 'random' or
    'greedy'. Creates nr_runs times a greedy or random rooster and plots the
    corresponding maluspoints in a histogram.
    '''

    #maluses = []
    random_dict = {}
    for i in range(nr_runs):
        my_rooster = Rooster(courses_df, student_df, rooms_df, evenings)
        my_rooster = Initialize(my_rooster)
        my_rooster.make_rooster_greedy()
        malus = sum(Evaluation(my_rooster).malus_count())
        random_dict[my_rooster] = malus

    lowest_rooster = min(random_dict, key=random_dict.get)
    result = Simulated_Annealing(lowest_rooster, initial_T).run()
    lowest_rooster = Hillclimber(result[1])
    lowest_rooster.hc_students('T')
    lowest_rooster.hc_students('P')

experiment(50)



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
