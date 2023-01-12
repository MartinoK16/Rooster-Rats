import random
import math
import pandas as pd
import numpy as np

# Melanie

# Output csv naar rooster per student
output_df = pd.read_csv('LecturesLesroosters/test.csv')
# Loop over the different rooms
count = 0
for student in output_df['student'].unique():
    # Get expected people of the rooms
    expected = output_df[output_df['student'] == student]
    #print(expected)

#---------------------------------------------------------------------------------------------------------
# Room class


#---------------------------------------------------------------------------------------------------------
# Room dictionary met aantal vakken

# Function to sort the list by second item of tuple
def Sort_Tuple(tup):
    """
    Accepts a list of tuples and sorts it using the second element in ascending
    order.
    """
    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of sublist lambda has been used
    return(sorted(tup, key = lambda x: x[1]))

sorted_rooms_with_capacity = Sort_Tuple(rooms_with_capacity)
# printing the sorted list of tuples
print(sorted_rooms_with_capacity)


# Create dictionary with room numbers as keys and empty lists as values
room_dictionary = dict.fromkeys(room_list, list())
room_dictionary = {room: [] for room in room_list}

print(f'Room dict is {room_dictionary}')

# Add courses to smallest room (lowest capacity) based on expected students
start_range = 0
for room, capacity in sorted_rooms_with_capacity:
    end_range = capacity

    for count, expected in enumerate(expected_list):
        if expected > start_range and expected <= end_range:
            room_dictionary[room].append(courses_list[count])
    start_range = end_range

print(room_dictionary)
