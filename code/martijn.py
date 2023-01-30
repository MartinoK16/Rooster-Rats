import time
import pickle
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from classes.rooster import *
from algorithms.evaluation import *
from algorithms.hillclimber import *
from algorithms.initialize import *
from algorithms.tabu_search import *

courses_df = pd.read_csv('../data/vakken.csv')
student_df = pd.read_csv('../data/studenten_en_vakken2.csv')
rooms_df = pd.read_csv('../data/zalen.csv')
evenings = {'C0.110'}
sys.setrecursionlimit(5000)

# my_rooster = Rooster(courses_df, student_df, rooms_df, evenings)
# my_rooster = Initialize(my_rooster)
# # my_rooster.make_rooster_random(4, 5, 7)
# my_rooster.make_rooster_greedy()
# # print(Evaluation(my_rooster).malus_count())
# # my_rooster = Hillclimber(my_rooster)
# # my_rooster.hc_activities()
# # my_rooster.hc_students('T')
# # my_rooster.hc_students('P')
# my_rooster = Tabu(my_rooster)
# my_rooster.tabu_search(100, 2000)
# print(my_rooster.iter[1])
#
# plt.plot(my_rooster.maluses)
# plt.plot(my_rooster.iter[0], my_rooster.iter[1], markersize=8, marker="o", markerfacecolor="red")
# plt.title('Tabu Search verloop minpunten')
# plt.xlabel('Iteraties')
# plt.ylabel('Minpunten')
# plt.show()



prev_malus = 65
maluses = []
for i in range(186, 1000):
    st = time.time()
    my_rooster = Rooster(courses_df, student_df, rooms_df, evenings)
    my_rooster = Initialize(my_rooster)
    # my_rooster.make_rooster_random(4, 5, 7)
    # my_rooster.make_rooster_largetosmall()
    my_rooster.make_rooster_greedy()
    malus = sum(Evaluation(my_rooster).malus_count())
    new_malus = malus - 1

    my_rooster = Hillclimber(my_rooster)
    while new_malus < malus:
        malus = sum(Evaluation(my_rooster).malus_count())
        my_rooster.hc_activities()
        my_rooster.hc_students('T')
        my_rooster.hc_students('P')
        new_malus = sum(Evaluation(my_rooster).malus_count())
        print(Evaluation(my_rooster).malus_count())

    print('Execution time malus:', time.time() - st, 'seconds')
    malus = Evaluation(my_rooster).malus_count()
    maluses.append(malus)
    print(maluses)
#
#     # if sum(malus) < prev_malus:
#     with open(f'RoosterWith{sum(malus)}Points_run{i+1}Test', 'wb') as outp:
#         pickle.dump(my_rooster, outp, pickle.HIGHEST_PROTOCOL)
#         prev_malus = sum(malus)
#
# for i in range(10, 1000):
#     with open(r'RoosterWith56Points_run82', 'rb') as input_file:
#         my_rooster = pickle.load(input_file)
#         malus = sum(Evaluation(my_rooster).malus_count())
#         malus_loop = [56, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#         while sum(malus_loop) < (len(malus_loop) * max(malus_loop)):
#         # for i in range(100):
#             my_rooster.hc_activities()
#             my_rooster.hc_students('T')
#             my_rooster.hc_students('P')
#             malus = sum(Evaluation(my_rooster).malus_count())
#             malus_loop.pop(0)
#             malus_loop.append(malus)
#             print(malus_loop, sum(malus_loop), len(malus_loop)*max(malus_loop))
#
#         # if malus < prev_malus:
#     with open(f'RoosterWith{malus}Points_refined56_run{i+1}', 'wb') as outp:
#         pickle.dump(my_rooster, outp, pickle.HIGHEST_PROTOCOL)
#             # prev_malus = malus
#
# with open(r'RoosterWith44Points_refined56_run0', 'rb') as input_file:
#     my_rooster = pickle.load(input_file)
#     Evaluation(my_rooster).make_csv('TESTCSV.csv')
#
#     my_rooster3 = Rooster(courses_df, student_df, rooms_df, evenings)
#     my_rooster2 = Evaluation(my_rooster3).rooster_object(rooster)
#     rooster2 = Evaluation(my_rooster2).rooster_dict()
#     print(rooster, rooster2)
#     if rooster == rooster2:
#         print('Bueno')
#
# my_rooster = Evaluation(my_rooster)
# my_rooster.make_csv('../data/Rooster60Points.csv')
# my_rooster.make_scheme()
#
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

# 186 Runs
# maluses = \
# [[63, 3, 5, 0], [65, 2, 10, 0], [55, 4, 10, 0], [65, 0, 5, 0], [95, 4, 5, 0], [65, \
# 5, 10, 0], [67, 5, 10, 0], [54, 3, 15, 0], [84, 9, 5, 0], [62, 1, 5, 0], [89, \
#  6, 5, 0], [80, 7, 10, 0], [79, 1, 5, 0], [59, 1, 5, 0], [73, 4, 10, 0], [74, 8, \
#  5, 0], [80, 7, 5, 0], [69, 10, 5, 0], [72, 0, 5, 0], [54, 4, 10, 0], [65, 0, 15 \
# , 0], [67, 1, 5, 0], [79, 3, 5, 0], [71, 1, 10, 0], [56, 3, 10, 0], [53, 4, 0, 0 \
# ], [70, 6, 10, 0], [70, 6, 10, 0], [79, 1, 0, 0], [74, 3, 5, 0], [68, 1, 15, 0], \
#  [65, 4, 10, 0], [56, 4, 20, 0], [52, 4, 10, 0], [49, 9, 20, 0], [62, 4, 5, 0], \
# [78, 8, 10, 0], [69, 1, 5, 0], [59, 3, 5, 0], [68, 2, 10, 0], [60, 6, 5, 0], [73 \
# , 2, 10, 0], [71, 5, 10, 0], [58, 3, 5, 0], [62, 7, 15, 0], [59, 0, 10, 0], [88, \
#  6, 0, 0], [71, 7, 5, 0], [74, 7, 5, 0], [61, 3, 5, 0], [79, 3, 5, 0], [65, 1, 5 \
# , 0], [51, 3, 10, 0], [80, 1, 0, 0], [85, 3, 0, 0], [56, 1, 10, 0], [54, 4, 10, \
# 0], [65, 5, 5, 0], [69, 6, 5, 0], [62, 0, 10, 0], [95, 5, 0, 0], [69, 3, 5, 0], \
# [80, 1, 15, 0], [64, 3, 10, 0], [89, 5, 5, 0], [66, 4, 5, 0], [71, 1, 10, 0], [68, \
#  3, 0, 0], [73, 4, 10, 0], [73, 1, 5, 0], [57, 0, 15, 0], [63, 4, 10, 0], [71, \
#  7, 10, 0], [72, 1, 5, 0], [86, 4, 10, 0], [73, 0, 10, 0], [55, 9, 10, 0], [74, \
# 2, 5, 0], [57, 5, 10, 0], [81, 5, 0, 0], [51, 7, 5, 0], [48, 3, 5, 0], [71, 4, 0 \
# , 0], [55, 3, 5, 0], [80, 4, 5, 0], [70, 5, 5, 0], [74, 2, 10, 0], [62, 5, 5, 0] \
# , [73, 6, 5, 0], [58, 7, 10, 0], [89, 6, 10, 0], [52, 6, 10, 0], [71, 0, 5, 0], \
# [62, 2, 10, 0], [91, 0, 10, 0], [74, 2, 5, 0], [54, 8, 10, 0], [64, 2, 0, 0], [61, \
#  2, 10, 0], [73, 4, 5, 0], [91, 4, 5, 0], [70, 4, 10, 0], [86, 1, 5, 0], [70, \
# 2, 5, 0], [66, 3, 10, 0], [64, 0, 5, 0], [66, 6, 10, 0], [68, 0, 5, 0], [57, 7, \
# 10, 0], [78, 5, 0, 0], [74, 6, 10, 0], [61, 0, 0, 0], [58, 3, 5, 0], [72, 6, 10, \
#  0], [91, 0, 10, 0], [68, 12, 5, 0], [72, 1, 10, 0], [75, 9, 0, 0], [78, 8, 5, 0 \
# ], [86, 5, 5, 0], [63, 3, 15, 0], [89, 3, 0, 0], [56, 4, 10, 0], [58, 2, 5, 0], \
# [60, 6, 5, 0], [93, 2, 0, 0], [73, 2, 10, 0], [64, 5, 5, 0], [80, 4, 10, 0], [63 \
# , 5, 10, 0], [71, 8, 10, 0], [64, 5, 10, 0], [62, 3, 10, 0], [67, 4, 5, 0], [60, \
#  6, 15, 0], [81, 4, 10, 0], [70, 4, 20, 0], [68, 3, 5, 0], [71, 2, 10, 0], [78, \
# 5, 10, 0], [61, 3, 5, 0], [43, 4, 20, 0], [69, 3, 5, 0], [54, 7, 5, 0], [88, 2, \
# 0, 0], [76, 8, 5, 0], [66, 2, 10, 0], [65, 7, 5, 0], [95, 2, 0, 0], [67, 1, 5, 0 \
# ], [75, 6, 5, 0], [66, 3, 10, 0], [67, 1, 10, 0], [61, 5, 5, 0], [67, 1, 5, 0], \
# [58, 3, 15, 0], [79, 1, 5, 0], [69, 1, 5, 0], [58, 5, 5, 0], [64, 1, 5, 0], [85, \
#  7, 5, 0], [62, 7, 10, 0], [64, 3, 15, 0], [66, 4, 5, 0], [68, 2, 10, 0], [52, 2 \
# , 15, 0], [67, 4, 10, 0], [60, 4, 10, 0], [72, 8, 10, 1], [68, 6, 10, 0], [81, 1, \
# 0, 5, 0], [75, 8, 10, 0], [54, 1, 15, 0], [67, 6, 10, 0], [75, 2, 5, 0], [76, 6, \
#  5, 0], [71, 4, 5, 0], [76, 2, 5, 0], [69, 2, 5, 0], [76, 2, 10, 0], [57, 2, 0, \
# 0], [57, 2, 15, 0], [59, 1, 5, 0], [77, 5, 15, 0], [57, 6, 10, 0], [74, 6, 5, 0]]
#
# sum_maluses = []
# for i in range(len(maluses)):
#     sum_maluses.append(sum(maluses[i]))
#
# sns.histplot(x=sum_maluses, binwidth=2, kde=True)
# plt.title(f'Verdeling minpunten van 186 hillclimber (studenten en activiteiten) roosters')
# plt.xlabel('Minpunten')
# plt.ylabel('Aantal')
# plt.show()
