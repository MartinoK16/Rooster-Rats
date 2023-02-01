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
student_df = pd.read_csv('../data/studenten_en_vakken.csv')
rooms_df = pd.read_csv('../data/zalen.csv')
evenings = {'C0.110'}
sys.setrecursionlimit(5000)

for i in range(100):
    my_rooster = Rooster(courses_df, student_df, rooms_df, evenings)
    my_rooster = Initialize(my_rooster)
    # my_rooster.make_rooster_random(4, 5, 7)
    my_rooster.make_rooster_greedy()
    # print(Evaluation(my_rooster).malus_count())
    # my_rooster = Hillclimber(my_rooster)
    # my_rooster.hc_activities()
    # my_rooster.hc_students('T')
    # my_rooster.hc_students('P')
    my_rooster = Tabu(my_rooster)
    my_rooster.tabu_search(100, 10000)
    print(my_rooster.iter[1])

    plt.plot(my_rooster.maluses)
    plt.plot(my_rooster.iter[0], my_rooster.iter[1], markersize=8, marker="o", markerfacecolor="red")
    plt.title('Tabu Search verloop minpunten')
    plt.xlabel('Iteraties')
    plt.ylabel('Minpunten')
    plt.grid(which='both')
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    # plt.savefig(f'Tabu_run{i}_{my_rooster.iter[1]}P.png')
    # # plt.show()
    # plt.close()

    with open(f'Tabu_run{i}', 'wb') as outp:
        pickle.dump(my_rooster, outp, pickle.HIGHEST_PROTOCOL)


# prev_malus = 65
# maluses = []
# for i in range(0, 100):
#     st = time.time()
#     my_rooster = Rooster(courses_df, student_df, rooms_df, evenings)
#     my_rooster = Initialize(my_rooster)
#     my_rooster.make_rooster_random(4, 5, 7)
#     # my_rooster.make_rooster_largetosmall()
#     # my_rooster.make_rooster_greedy()
#     malus = sum(Evaluation(my_rooster).malus_count())
#     new_malus = malus - 1
#
#     my_rooster = Hillclimber(my_rooster)
#     while new_malus < malus:
#         malus = sum(Evaluation(my_rooster).malus_count())
#         my_rooster.hc_activities()
#         my_rooster.hc_students('T')
#         my_rooster.hc_students('P')
#         new_malus = sum(Evaluation(my_rooster).malus_count())
#         print(Evaluation(my_rooster).malus_count())
#
#     print('Execution time malus:', time.time() - st, 'seconds')
#     malus = Evaluation(my_rooster).malus_count()
#     maluses.append(malus)
#     print(i, maluses)
#
#     if sum(malus) < prev_malus:
#     with open(f'RoosterWith{sum(malus)}Points_run{i+1}', 'wb') as outp:
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

# 200 Runs Greedy Hillclimber + students
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
# 0], [57, 2, 15, 0], [59, 1, 5, 0], [77, 5, 15, 0], [57, 6, 10, 0], [74, 6, 5, 0], \
# [57, 8, 5, 0], [64, 0, 15, 0], [80, 4, 5, 0], [68, 3, 5, 0], [72, 10, 5, 0], [78, \
#  6, 5, 0], [62, 10, 10, 0], [68, 6, 10, 0], [68, 2, 20, 0], [70, 2, 10, 0], [89, \
# 5, 0, 0], [76, 1, 15, 0], [80, 3, 5, 0], [64, 2, 10, 0]]

# 200 Runs Greedy Hillclimber
# maluses = \
# [[154, 14, 10, 0], [141, 13, 20, 0], [144, 13, 10, 0], [161, 7, 20, 0], [168 \
# , 25, 5, 0], [162, 12, 5, 0], [151, 6, 15, 0], [170, 6, 0, 0], [134, 16, 15, 0], \
#  [149, 8, 15, 0], [154, 6, 10, 0], [140, 24, 15, 0], [159, 15, 5, 0], [157, 24, \
# 15, 0], [171, 20, 10, 0], [152, 19, 15, 0], [161, 19, 5, 0], [163, 24, 10, 0], [ \
# 149, 23, 10, 0], [116, 9, 20, 0], [144, 18, 10, 0], [136, 15, 10, 0], [177, 23, \
# 10, 0], [158, 23, 10, 0], [191, 13, 5, 0], [177, 18, 5, 0], [137, 7, 15, 0], [156 \
# , 18, 15, 0], [151, 12, 5, 0], [152, 19, 15, 0], [166, 26, 5, 0], [138, 22, 15, \
#  0], [152, 25, 10, 0], [139, 14, 15, 0], [153, 28, 10, 0], [151, 9, 10, 0], [147 \
# , 11, 5, 0], [139, 13, 10, 0], [167, 15, 5, 0], [143, 10, 15, 0], [135, 31, 10, \
# 0], [165, 15, 5, 0], [169, 12, 15, 0], [157, 7, 10, 0], [161, 15, 10, 0], [151, \
# 17, 10, 0], [149, 16, 10, 0], [141, 12, 10, 0], [133, 10, 20, 0], [153, 8, 5, 0] \
# , [144, 7, 15, 0], [150, 32, 5, 0], [136, 9, 10, 0], [158, 16, 5, 0], [156, 18, \
# 20, 0], [187, 21, 5, 0], [186, 23, 10, 0], [163, 18, 15, 0], [157, 18, 10, 0], [ \
# 176, 6, 5, 0], [149, 8, 10, 0], [143, 9, 15, 0], [154, 14, 10, 0], [145, 7, 10, \
# 0], [167, 12, 10, 0], [176, 20, 5, 0], [163, 13, 10, 0], [141, 26, 10, 0], [150, \
#  14, 10, 0], [160, 11, 10, 0], [150, 17, 10, 0], [135, 14, 5, 0], [131, 9, 20, 0 \
# ], [168, 11, 5, 0], [144, 10, 10, 0], [168, 9, 10, 0], [140, 14, 15, 0], [167, 19 \
# , 5, 0], [160, 24, 15, 0], [159, 11, 5, 0], [178, 10, 10, 0], [176, 26, 0, 0], \
# [159, 12, 10, 0], [162, 7, 5, 0], [139, 15, 10, 0], [172, 25, 5, 0], [154, 12, 5 \
# , 0], [140, 21, 15, 0], [147, 25, 10, 0], [144, 16, 15, 0], [143, 8, 15, 0], [159 \
# , 15, 10, 0], [157, 9, 10, 0], [150, 23, 15, 0], [175, 18, 5, 0], [150, 6, 10, \
# 0], [154, 8, 5, 0], [173, 23, 10, 0], [161, 16, 10, 0], [158, 13, 5, 0], [148, 9 \
# , 15, 0], [131, 20, 10, 0], [158, 15, 10, 0], [159, 12, 0, 0], [160, 11, 5, 0], \
# [144, 11, 20, 0], [164, 16, 10, 0], [165, 11, 5, 0], [157, 26, 5, 0], [158, 14, \
# 10, 0], [172, 21, 5, 0], [161, 11, 15, 0], [148, 17, 15, 0], [166, 30, 10, 0], [ \
# 168, 13, 5, 0], [157, 6, 5, 0], [150, 17, 5, 0], [165, 16, 0, 0], [129, 18, 5, 0 \
# ], [172, 18, 5, 0], [173, 13, 5, 0], [171, 15, 15, 0], [160, 17, 15, 0], [141, 12 \
# , 15, 0], [148, 8, 15, 0], [157, 15, 10, 0], [166, 14, 5, 0], [151, 18, 20, 0], \
#  [149, 16, 15, 0], [164, 16, 10, 0], [141, 12, 5, 0], [155, 6, 10, 0], [124, 15, \
#  10, 0], [149, 6, 5, 0], [173, 16, 10, 0], [169, 16, 5, 0], [144, 19, 10, 0], [176 \
# , 26, 0, 0], [166, 15, 10, 0], [154, 12, 5, 0], [154, 7, 0, 0], [158, 9, 5, 0] \
# , [128, 7, 15, 0], [136, 19, 5, 0], [157, 17, 15, 0], [162, 21, 0, 0], [140, 12, \
#  5, 0], [164, 34, 10, 0], [141, 10, 5, 0], [154, 24, 15, 0], [155, 15, 20, 0], [ \
# 160, 10, 10, 0], [167, 13, 10, 0], [127, 11, 15, 0], [168, 18, 15, 0], [165, 5, \
# 5, 0], [143, 7, 10, 0], [132, 19, 15, 0], [167, 31, 0, 0], [124, 6, 15, 0], [152 \
# , 18, 10, 0], [188, 31, 5, 0], [166, 26, 5, 0], [143, 8, 15, 0], [136, 13, 5, 0] \
# , [143, 19, 5, 0], [143, 6, 5, 0], [154, 17, 15, 0], [144, 12, 20, 0], [143, 9, \
# 10, 0], [140, 21, 10, 0], [160, 11, 5, 0], [176, 20, 5, 0], [159, 18, 10, 0], [162 \
# , 17, 5, 0], [183, 24, 0, 0], [138, 12, 10, 0], [165, 9, 15, 0], [157, 15, 10, \
#  0], [182, 23, 0, 0], [169, 30, 5, 0], [171, 6, 5, 0], [172, 13, 0, 0], [154, 16 \
# , 5, 0], [148, 21, 5, 0], [163, 16, 10, 0], [164, 15, 10, 0], [148, 9, 10, 0], [ \
# 148, 12, 15, 0], [158, 23, 10, 0], [161, 16, 5, 0], [160, 15, 10, 0], [146, 15, \
# 15, 0], [148, 8, 5, 0], [161, 14, 5, 0], [160, 16, 5, 0], [151, 14, 10, 0], [173 \
# , 17, 5, 0], [154, 12, 15, 0], [146, 18, 10, 0]]
#
# 209 Runs Random + Hillclimber + students
# maluses = \
# [[72, 2, 5, 0], [112, 2, 0, 1], [85, 0, 10, 1], [81, 5, 15, 2], [94, 1, 5, 1] \
# , [63, 4, 10, 1], [76, 3, 5, 1], [97, 1, 5, 1], [87, 5, 10, 2], [76, 6, 10, 12], \
#  [80, 3, 10, 12], [74, 5, 10, 0], [72, 3, 5, 13], [99, 1, 5, 1], [77, 1, 10, 1], \
#  [79, 1, 10, 0], [64, 0, 10, 1], [85, 8, 10, 1], [101, 11, 5, 1], [71, 3, 10, 2] \
# , [86, 4, 5, 1], [76, 8, 0, 0], [69, 2, 10, 0], [76, 8, 15, 14], [74, 4, 10, 2], \
#  [89, 3, 5, 1], [98, 5, 0, 2], [77, 12, 10, 0], [71, 9, 15, 0], [61, 3, 5, 1], [ \
# 67, 13, 15, 0], [86, 1, 5, 0], [82, 5, 5, 1], [86, 5, 5, 0], [83, 1, 10, 1], [77 \
# , 6, 10, 1], [85, 2, 5, 13], [72, 2, 5, 1], [89, 12, 10, 0], [78, 3, 10, 1], [72 \
# , 8, 10, 0], [73, 2, 5, 0], [74, 0, 10, 0], [96, 6, 5, 0], [91, 2, 0, 0], [91, 4 \
# , 5, 0], [71, 2, 5, 13], [76, 3, 10, 1], [86, 5, 0, 0], [80, 1, 5, 0], [73, 3, 15 \
# , 0], [62, 3, 5, 0], [86, 5, 0, 0], [85, 9, 15, 0], [51, 3, 5, 1], [60, 5, 10, \
# 0], [75, 3, 10, 14], [72, 2, 10, 1], [66, 1, 15, 0], [68, 4, 10, 12], [65, 3, 10 \
# , 1], [74, 1, 10, 1], [107, 3, 0, 0], [101, 0, 5, 1], [94, 4, 0, 1], [96, 2, 5, \
# 1], [76, 5, 15, 1], [61, 0, 15, 0], [56, 13, 20, 0], [93, 4, 5, 1], [83, 5, 10, 0], [96, 3, 5, 2], [70, 6, 10, 1], [82, 2, 10, 0], [76, 5, 5, 1], [88, 3, 10, 0], [61, 3, 15, 0], [96, 4, 10, 1], [93, 2, 0, 0], [85, 4, 10, 0], [61, \
#  2, 5, 13], [87, 4, 5, 1], [74, 4, 15, 1], [64, 2, 5, 0], [94, 2, 10, 13], [99, 5, 0, 1], [78, 2, 10, 0], [78, 3, 5, 0], [93, 2, 5, 0], [100, 4, 5, 2], [71, 3, 10, 0], [75, 2, 10, 1], [79, 4, 5, 1], [91, 2, 5, \
# 0], [88, 3, 5, 0], [90, 7, 10, 0], [85, 2, 10, 0], [97, 7, 0, 13], [73, 5, 5, 14], [87, 8, 5, 0], [81, 5, 0, 12], [77, 3, 5, 0], [83, 4, 10, 0], [91, 4, 5, 1], [67, 1, 10, 0], [64, 1, 5, 0], [70, 3, 5, 0], [66, \
#  0, 5, 12], [80, 1, 0, 0], [89, 1, 10, 1], [94, 1, 5, 1], [69, 1, 10, 0], [82, 0, 5, 1], [71, 1, 5, 0], [89, 0, 0, 1], [93, 5, 0, 12], [78, 4, 10, 0], [77, 6, 5, 0], [86, 4, 10, 0], [97, 6, 0, 0], [80, 6, 10, 0 \
# ], [81, 4, 10, 1], [88, 8, 5, 1], [88, 4, 10, 12], [95, 1, 10, 0], [77, 4, 5, 1], [80, 2, 5, 0], [85, 2, 5, 12], [97, 2, 0, 0], [93, 0, 0, 0], [106, 5, 0, 12], [114, 0, 0, 0], [84, 3, 10, 1], [105, 2, 0, 1], [67 \
# , 1, 10, 0], [87, 7, 15, 0], [88, 1, 5, 1], [91, 7, 5, 1], [85, 4, 5, 0], [59, 3, 5, 0], [79, 1, 15, 1], [84, 5, 0, 0], [96, 1, 10, 1], [74, 3, 5, 2], [67, 3, 10, 2], [71, 7, 5, 0], [94, 4, 5, 0], [74, 4, 10, \
# 15], [58, 1, 10, 12], [98, 2, 5, 1], [87, 4, 10, 0], [72, 8, 5, 1], [86, 5, 10, 0], [81, 3, 5, 1], [99, 3, 5, 1], [75, 0, 0, 12], [81, 4, 15, 12], [61, 3, 10, 1], [81, 3, 15, 1], [84, 3, 5, 0], [79, 1, 15, 12], \
#  [90, 0, 5, 1], [85, 11, 15, 1], [68, 1, 15, 1], [76, 4, 10, 1], [76, 2, 15, 0], [74, 10, 0, 12], [87, 7, 5, 1], [96, 5, 0, 1], [79, 2, 10, 12], [77, 3, 10, 2], [78, 3, 5, 13], [76, 1, 5, 0], [64, 0, 10, 0], [75 \
# , 2, 5, 0], [84, 5, 5, 0], [74, 1, 5, 0], [92, 6, 10, 0], [89, 8, 5, 1], [84, 1, 5, 1], [114, 2, 0, 1], [88, 3, 0, 1], [64, 5, 15, 0], [91, 1, 0, 0], [86, 9, 0, 0], [69, 2, 5, 12], [78, 2, 0, 1], [77, 2, 5, 0] \
# , [72, 9, 10, 0], [86, 12, 0, 0], [67, 0, 10, 0], [93, 6, 5, 1], [69, 9, 10, 0], [87, 6, 5, 0], [73, 1, 15, 0], [92, 3, 0, 0], [78, 18, 10, 1], [78, 6, 15, 0], [66, 1, 10, 0], [127, 6, 5, 2]] #, [82, 10, 10, 2], [ \
# # 105, 0, 0, 1], [92, 2, 5, 1], [101, 0, 5, 0], [94, 9, 0, 15], [80, 6, 5, 0], [68, 2, 5, 1], [90, 3, 0, 0], [110, 5, 0, 0]]
#
#
# sum_maluses = []
# for i in range(len(maluses)):
#     sum_maluses.append(sum(maluses[i]))
#     print([i])
# print(np.std(sum_maluses))
# print(np.mean(sum_maluses))
# print(np.min(sum_maluses))
# print(np.max(sum_maluses))
#
# sns.histplot(x=sum_maluses, binwidth=2, kde=True)
# plt.title(f'Verdeling minpunten van 200 greedy hillclimber (activiteiten + studenten) roosters')
# plt.xlabel('Minpunten')
# plt.ylabel('Aantal')
# plt.show()
#
#
# with open(r'RoosterWith44Points_refined56_run0', 'rb') as input_file:
#     my_rooster = pickle.load(input_file)
#     # Evaluation(my_rooster).make_scheme()
#     # for stud in my_rooster.students:
#     #     if sum(stud.malus) > 0:
#     #         print(stud.nr, stud.malus, len(stud.courses))
#     Evaluation(my_rooster).make_csv('TESTCSV44')
#
# print()
# with open(r'RoosterWith94Points_run129', 'rb') as input_file:
#     my_rooster = pickle.load(input_file)
#     for stud in my_rooster.students:
#         if sum(stud.malus) > 0:
#             print(stud.nr, stud.malus, len(stud.courses))
