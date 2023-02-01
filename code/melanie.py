import random
import math
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from classes.rooster import Rooster
from classes.room import Room
from student_rooster import rooster_per_student
from algorithms.initialize import *
from algorithms.hillclimber import *


# # Create output csv
# my_rooster4.make_csv('../data/rooster_v4.csv')

courses_df = pd.read_csv('../data/vakken.csv')
student_df = pd.read_csv('../data/studenten_en_vakken2.csv')
rooms_df = pd.read_csv('../data/zalen.csv')

# Rooms with evening timeslot
evenings = {'C0.110REMOVE'}


def hc_students(self, tut_or_prac):
    """
    Accepts a string, 'T' for tutorial or 'P' for practical, and moves or
    swaps students to another tutorial group or practical group, based on a
    decreasing number of malus points.
    """
    for nr, course in enumerate(random.sample(self.courses, len(self.courses))): # Ga alle vakken langs         # ENUMERATE WEGHALEN
        nr_werk_groups = len(getattr(course, tut_or_prac))

        for group in getattr(course, tut_or_prac):
            group_nr = int(group.type[1])

            for student in group.studs:
                tries = {} # key = group nr, value = malus
                tries2 = {} # key = list of group nr and student index; value = malus
                malus = sum(Evaluation(self).malus_count())
                tries[group_nr] = malus
                tries2[student] = malus

                for i in range(nr_werk_groups):
                    new_group_nr = i + 1
                    new_group = getattr(course, tut_or_prac)[i]

                    if new_group_nr != group_nr and new_group.max_studs > new_group.size: # Houd rekening met maximale aantal studenten per werkgroep
                        self.move_student(student, group, group.slot, new_group, new_group.slot)
                        tries[new_group_nr] = sum(Evaluation(self).malus_count()) # Maluspunten voor eventuele nieuwe groep
                        self.move_student(student, new_group, new_group.slot, group, group.slot)

                    if new_group_nr != group_nr:
                        for nr1, other_student in enumerate(new_group.studs):
                            self.swap_student(student, group, group.slot, other_student, new_group, new_group.slot)
                            tries2[(new_group_nr, other_student)] = sum(Evaluation(self).malus_count())
                            self.swap_student(other_student, group, group.slot, student, new_group, new_group.slot)

                best_move_nr = random.choice([k for k, v in tries.items() if v==min(tries.values())]) # Select group in which the student can best be placed
                move_malus = tries[best_move_nr]
                best_move = getattr(course, tut_or_prac)[best_move_nr - 1]

                best_swap_try = random.choice([k for k, v in tries2.items() if v==min(tries2.values())]) # Select group in which the student can best be placed

                # Als de originele maluscount (met key = studentnummer) niet de laagste is bij swappen
                if best_swap_try != student:
                    best_swap_nr = best_swap_try[0] # Correct group to swap the student to
                    best_swap_stud = best_swap_try[1] # Index to search the right student
                    swap_malus = tries2[best_swap_try]
                    best_swap = getattr(course, tut_or_prac)[best_swap_nr - 1]

                    # Als moven tot het laagste aantal maluspoints leidt
                    if best_move_nr != group_nr and move_malus <= swap_malus:
                        self.move_student(student, group, group.slot, best_move, best_move.slot)
                    # Als swappen tot het laagste aantal maluspoints leidt
                    elif best_swap_nr != group_nr:
                        self.swap_student(student, group, group.slot, best_swap_stud, best_swap, best_swap.slot)

                # Als de originele maluscount (met key = studentnummer) de laagste is bij swappen
                else:
                    if best_move_nr != group_nr and move_malus <= tries2[student]:
                        self.move_student(student, group, group.slot, best_move, best_move.slot)

        # malus = Evaluation(self).malus_count()
        # print(malus, malus, nr, tut_or_prac)


def make_plot(nr_runs=20, type_rooster='random', algorithm='hc_activities', separated=False, rep=1):
    '''
    Accepts three optional arguments:
    · nr_runs = integer
    · type_rooster = 'random', 'greedy', 'large to small'
    · hc_activities = 'hc_activities', 'hc_students', 'hc_activities_and_students'
    · separated = boolean; tells if the malus counts are shown separately or as their sum
    Keeps track of malus count per iteration for each run and creates a lineplot
    of the average, minimum and maximum malus count per iteration.
    '''
    if separated == False:
        malus_lists = []
        avg_maluses = []
        min_maluses = []
        max_maluses = []
    else:
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

        for i in range(rep):

            if algorithm == 'hc_activities':
                my_rooster.hc_activities()
            elif algorithm == 'hc_students':
                my_rooster.hc_students('T')
                my_rooster.hc_students('P')
            else:
                my_rooster.hc_activities()
                my_rooster.hc_students('T')
                my_rooster.hc_students('P')

        if separated == False:
            malus_lists.append(my_rooster.maluses)
        else:
            malus_lists_0.append([item[0] for item in my_rooster.separated_maluses])
            malus_lists_1.append([item[1] for item in my_rooster.separated_maluses])
            malus_lists_2.append([item[2] for item in my_rooster.separated_maluses])
            malus_lists_3.append([item[3] for item in my_rooster.separated_maluses])

        # iterations = my_rooster.iterations
    if separated == False:
        for j in range(len(malus_lists[0])):
            combine_numbers = [item[j] for item in malus_lists]
            avg_maluses.append(np.mean(combine_numbers))
            min_maluses.append(np.min(combine_numbers))
            max_maluses.append(np.max(combine_numbers))
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

    if separated == False:
        plt.fill_between(x=np.linspace(1, len(malus_lists[0]), num=len(malus_lists[0])), y1=min_maluses, y2=max_maluses, alpha=0.4)
        plt.plot(np.linspace(1, len(malus_lists[0]), num=len(malus_lists[0])), avg_maluses)
    else:
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

make_plot(nr_runs=20, type_rooster='random', separated=False, algorithm='hc_activities', rep=1)

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

# def move_student(self, student, lec1, slot1, lec2, slot2):
#     '''
#     Removes a student from a lecture and adds it to another one.
#     Also updates the student rooster and malus points
#     '''
#     lec1.studs.remove(student)
#     lec1.size -= 1
#     lec1.room.update_malus()
#     lec2.studs.append(student)
#     lec2.size += 1
#     lec2.room.update_malus()
#     # Remove lec1 and add lec2 to student rooster
#     student.swap_lecture(lec1, slot1, lec2, slot2)


# Melanie

# # Output csv naar rooster per student
# output_df = pd.read_csv('../data/random_rooster.csv')
#
# # Loop over the different students
# for student in output_df['student'].unique():
#     rooster_data = output_df[output_df['student'] == student]
#
#     # Create empty rooster
#     stud_rooster = np.zeros((5,5), dtype=object)
#     # Houd aantal vakken bij
#     nr_vakken = 0
#
#     # Studentnummer
#     print("")
#     print(student)
#
#     # Create rooster voor deze student
#     for _, row in rooster_data.iterrows():
#         # Informatie van het in te plannen vak
#         vak = row['vak']
#         activiteit = row['activiteit']
#         zaal = row['zaal']
#
#         day_dict = {'ma': 0, 'di': 1, 'wo': 2, 'do': 3, 'vr': 4, 'za': 5, 'zo': 6}
#
#         # Indices (dag en tijdslot) voor rooster creëren, m.b.v. bovenstaande dict
#         dag = row['dag']
#         dag_index = day_dict[dag]
#         tijdslot = row['tijdslot']
#         tijdslot_index = int((tijdslot - 9) / 2)
#
#         # Plak informatie van het in te plannen vak achter elkaar als string
#         rooster_data_string = f'{vak}, {activiteit}, {zaal}'
#
#         # Plan vak(ken) als list in op het gewenste moment
#         if stud_rooster[tijdslot_index, dag_index] == 0:
#             stud_rooster[tijdslot_index, dag_index] = [rooster_data_string]
#         # Meerdere vakken per list in het geval van overlap
#         else:
#             stud_rooster[tijdslot_index, dag_index].append(rooster_data_string)
#
#         nr_vakken += 1
#
#         # Informatie van het ingeplande vak
#         print(rooster_data_string)
#
#     # Aantal vakken en gemaakte rooster voor deze student
#     print(nr_vakken)
#     print(stud_rooster)


#---------------------------------------------------------------------------------------------------------
# Room class
# class Room():
#     def __init__(self, nr_timeslots, nr_days, room, evening, room_capacity):
#         self.nr_timeslots = nr_timeslots # Standard; without evening timeslot
#         self.nr_days = nr_days
#         self.room = room # object or integer
#         self.evening = evening # boolean
#         self.capacity = room_capacity
#
#         # Create first version of rooster and availability
#         if self.evening:
#             self.availability = np.zeros((nr_timeslots + 1, nr_days))
#             self.rooster = np.zeros((nr_timeslots + 1, nr_days))
#         else:
#             self.availability = np.zeros((nr_timeslots, nr_days))
#             self.rooster = np.zeros((nr_timeslots, nr_days))
#
#     def check_availability(self):
#         """
#         Accepts a 3D array of shape nr_rooms x nr_days x nr_timeslots and checks the
#         availability for a given room. The function returns a boolean 3D array of
#         shape nr_days x nr_timeslots which shows if the timeslot is occupied (True)
#         or not (False).
#         """
#         # Check availability for the room; switch True and False (occupied = 1; not occupied = 0)
#         self.availability = np.invert(self.rooster == self.availability)
#
#     def remove_course(self, timeslot, day):
#         self.rooster[day, timeslot] = 0
#
#     def add_course(self, course, timeslot, day):
#         self.rooster[day, timeslot] = course
#
# room_obj = Room(4, 5, 1, True, 120)
# room_obj.check_availability()
# print(room_obj.availability)
# room_obj.add_course(38, 2, 3)
# print(room_obj.rooster)
# room_obj.check_availability() # Werkt niet
# print(room_obj.availability)
# #---------------------------------------------------------------------------------------------------------
# # Room dictionary met aantal vakken
#
# # Create list of DataFrame column
# def select_data(file, column_name):
#     df = pd.read_csv(file)
#     data_list = df[column_name].values.tolist()
#     return data_list
#
# capacity_list = select_data("data/zalen.csv", "Max. capaciteit")
# expected_list = select_data("data/vakken.csv", "Verwacht")
# room_list = select_data("data/zalen.csv", "Zaalnummber")
# courses_list = select_data("data/vakken.csv", "Vak")
#
# print(capacity_list)
# print(expected_list)
# print(room_list)
# print(courses_list)
#
# rooms_with_capacity = list(zip(room_list, capacity_list))
#
#
# # Function to sort the list by second item of tuple
# def Sort_Tuple(tup):
#     """
#     Accepts a list of tuples and sorts it using the second element in ascending
#     order.
#     """
#     # reverse = None (Sorts in Ascending order)
#     # key is set to sort using second element of sublist lambda has been used
#     return(sorted(tup, key=lambda x: x[1]))
#
#
# sorted_rooms_with_capacity = Sort_Tuple(rooms_with_capacity)
# # printing the sorted list of tuples
# print(sorted_rooms_with_capacity)
#
#
# # Create dictionary with room numbers as keys and empty lists as values
# room_dictionary = dict.fromkeys(room_list, list())
# room_dictionary = {room: [] for room in room_list}
#
# print(f'Room dict is {room_dictionary}')
#
# # Add courses to smallest room (lowest capacity) based on expected students
# start_range = 0
# for room, capacity in sorted_rooms_with_capacity:
#     end_range = capacity
#
#     for count, expected in enumerate(expected_list):
#         if expected > start_range and expected <= end_range:
#             room_dictionary[room].append(courses_list[count])
#     start_range = end_range
#
# print(room_dictionary)
