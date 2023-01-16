import random
import math
import pandas as pd
import numpy as np

# Melanie

# Output csv naar rooster per student
output_df = pd.read_csv('../data/random_rooster.csv')

# Loop over the different students
for student in output_df['student'].unique():
    rooster_data = output_df[output_df['student'] == student]

    # Create empty rooster
    stud_rooster = np.zeros((5,5), dtype=object)
    # Houd aantal vakken bij
    nr_vakken = 0

    # Studentnummer
    print("")
    print(student)

    # Create rooster voor deze student
    for _, row in rooster_data.iterrows():
        # Informatie van het in te plannen vak
        vak = row['vak']
        activiteit = row['activiteit']
        zaal = row['zaal']

        day_dict = {'ma': 0, 'di': 1, 'wo': 2, 'do': 3, 'vr': 4, 'za': 5, 'zo': 6}

        # Indices (dag en tijdslot) voor rooster creëren, m.b.v. bovenstaande dict
        dag = row['dag']
        dag_index = day_dict[dag]
        tijdslot = row['tijdslot']
        tijdslot_index = int((tijdslot - 9) / 2)

        # Plak informatie van het in te plannen vak achter elkaar als string
        rooster_data_string = f'{vak}, {activiteit}, {zaal}'

        # Plan vak(ken) als list in op het gewenste moment
        if stud_rooster[tijdslot_index, dag_index] == 0:
            stud_rooster[tijdslot_index, dag_index] = [rooster_data_string]
        # Meerdere vakken per list in het geval van overlap
        else:
            stud_rooster[tijdslot_index, dag_index].append(rooster_data_string)

        nr_vakken += 1

        # Informatie van het ingeplande vak
        print(rooster_data_string)

    # Aantal vakken en gemaakte rooster voor deze student
    print(nr_vakken)
    print(stud_rooster)


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
