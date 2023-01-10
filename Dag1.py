import pandas as pd

# Create list of DataFrame column
def select_data(file, column_name):
    df = pd.read_csv(file)
    data_list = df[column_name].values.tolist()
    return data_list

capacity_list = select_data("LecturesLesroosters/zalen.csv", "Max. capaciteit")
expected_list = select_data("LecturesLesroosters/vakken.csv", "Verwacht")
room_list = select_data("LecturesLesroosters/zalen.csv", "Zaalnummber")
courses_list = select_data("LecturesLesroosters/vakken.csv", "Vak")

print(capacity_list)
print(expected_list)
print(room_list)
print(courses_list)

rooms_with_capacity = list(zip(room_list, capacity_list))
print(rooms_with_capacity)




# Python program to sort a list of tuples by the second Item using sorted()
# https://www.geeksforgeeks.org/python-program-to-sort-a-list-of-tuples-by-second-item/

# Function to sort the list by second item of tuple
def Sort_Tuple(tup):

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
