import time
import pickle
import sys
import pandas as pd
from classes.rooster import Rooster
from algorithms.evaluation import *
from algorithms.hillclimber import *
from algorithms.initialize import *

courses_df = pd.read_csv('../data/vakken.csv')
student_df = pd.read_csv('../data/studenten_en_vakken2.csv')
rooms_df = pd.read_csv('../data/zalen.csv')
evenings = {'C0.110'}
sys.setrecursionlimit(5000)


# prev_malus = 61
# maluses = []
# for i in range(1000):
#     st = time.time()
#     my_rooster = Rooster(courses_df, student_df, rooms_df, evenings)
#     my_rooster = Initialize(my_rooster)
#     # my_rooster.make_rooster_random(4, 5, 7)
#     # my_rooster.make_rooster_largetosmall()
#     my_rooster.make_rooster_greedy()
#     malus = sum(Evaluation(my_rooster).malus_count())
#     new_malus = malus - 1
#
#     my_rooster = Hillclimber(my_rooster)
#     while new_malus < malus:
#         malus = sum(Evaluation(my_rooster).malus_count())
#         my_rooster.lectures()
#         my_rooster.students('W')
#         my_rooster.students('P')
#         new_malus = sum(Evaluation(my_rooster).malus_count())
#         print(Evaluation(my_rooster).malus_count())
#
#     print('Execution time malus:', time.time() - st, 'seconds')
#     malus = Evaluation(my_rooster).malus_count()
#     maluses.append(malus)
#     print(maluses)
#
#     if sum(malus) < prev_malus:
#         with open(f'RoosterWith{sum(malus)}Points', 'wb') as outp:
#             pickle.dump(my_rooster, outp, pickle.HIGHEST_PROTOCOL)
#         prev_malus = sum(malus)

with open(r'RoosterWith60Points', 'rb') as input_file:
    my_rooster = pickle.load(input_file)
print(my_rooster)

# my_rooster = Evaluation(my_rooster)
# my_rooster.make_csv('../data/Rooster60Points')
# my_rooster.make_scheme()

# my_rooster = Hillclimber(my_rooster)
# malus = sum(Evaluation(my_rooster).malus_count())
# my_rooster.lectures()
# my_rooster.students('W')
# my_rooster.students('P')
# malus = Evaluation(my_rooster).malus_count()
# print(malus)
#
# if sum(malus) <= 60:
#     with open(f'RoosterWith{sum(malus)}Points', 'wb') as outp:
#         pickle.dump(my_rooster, outp, pickle.HIGHEST_PROTOCOL)
#     prev_malus = sum(malus)

# maluses = []
# my_rooster = Rooster(courses_df, student_df, rooms_df, evenings)
# for i in range(5000):
#     my_rooster.make_rooster_random(4, 5, 7)
#     my_rooster.malus_count()
#     maluses.append(sum(my_rooster.malus))
#
# sns.histplot(x=maluses, binwidth=20, kde=True)
# plt.show()
