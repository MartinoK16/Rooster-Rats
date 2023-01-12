import random
import math
import pandas as pd
import numpy as np

class Lecture():
    def __init__(self, lecture_name, lecture_type, lecture_studs, class_nr):
        # Give the lecture its name, type, lecture code and student numbers
        d = {'H': 1, 'W': 2, 'P': 3}
        self.name = lecture_name
        self.type = lecture_type
        self.studs = lecture_studs
        self.code = int(f'{class_nr + 11}{d[lecture_type[0]]}{lecture_type[1]}')
        # print(self.code)
        # print(self.name)
        # print(self.type)
        # print(self.studs)

class Course():
    def __init__(self, course, student_list, class_nr):
        # Give for every course its name, #hoor, max studs werk, max studs prac and the student list for this course
        self.name = course[0]
        self.hoor = course[1]
        self.werk = course[2]
        self.prac = course[3]
        self.lectures = []
        self.students = random.sample(student_list, len(student_list))

        # Make a lecture for each hoorcollege with all the students
        for nr in range(self.hoor):
            self.lectures.append(Lecture(self.name, f'H{nr + 1}', self.students, class_nr))

        # Nr of werkcolleges and groups of students per werkcollege and make a lecture of it
        rooms = 0
        if self.werk > 0:
            rooms = math.ceil(len(self.students) / self.werk)
        for nr in range(rooms):
            nr_students = len(self.students) // rooms
            self.lectures.append(Lecture(self.name, f'W{nr + 1}', self.students[nr * nr_students:(nr + 1) * nr_students], class_nr))

        # Nr of practica and groups of students per practica and make a lecture of it
        rooms = 0
        if self.prac > 0:
            rooms = math.ceil(len(self.students) / self.prac)
        for nr in range(rooms):
            nr_students = len(self.students) // rooms
            self.lectures.append(Lecture(self.name, f'P{nr + 1}', self.students[nr * nr_students:(nr + 1) * nr_students], class_nr))

class Rooster():
    def __init__(self, courses_list, student_df):
        self.courses = []

        # Loop over all the courses needed for the rooster
        for nr, course in enumerate(courses_list):
            # Replace NaN with 0
            course[1:] = [0 if math.isnan(i) else i for i in course[1:]]

            # Loop over the students to see who has this course and add it to the student list
            student_list = []
            for _, student in student_df.iterrows():
                if course[0] in student['Vakken']:
                    student_list.append(student['Stud.Nr.'])

            # Add the course to the rooster
            self.courses.append(Course(course, student_list, nr))


def lecture_count(file):
    df = pd.read_csv(file)
    courses_list = []

    for _, row in df.iterrows():
        courses_list.append([row['Vak'], row['#Hoorcolleges'], row['Max. stud. Werkcollege'], row['Max. stud. Practicum']])

    return courses_list


def make_rooster_random(codes_list, hours, days, rooms):
    # Make a zeros array with the correct length
    rooster = np.zeros(hours * days * rooms)
    # Get the indices where the lectures will be planned
    slots = random.sample(range(hours * days * rooms), len(codes_list))
    # Put the lecture in the deterimined spot
    for nr, slot in enumerate(slots):
        rooster[slot] = codes_list[nr]
    # Reshape the 1D array to a 3D array for clarity
    return rooster.reshape((rooms, hours, days))


# Returns a list with Name, #Hoorcolleges, Max Stud Werkcollege, Max Stud Practicum
courses_list = lecture_count('LecturesLesroosters/vakken.csv')

# Make a Rooster object with the courses and students DataFrame
my_rooster = Rooster(courses_list, pd.read_csv('LecturesLesroosters/studenten_en_vakken2.csv'))

# Get all the lecture codes form the rooster Class
codes = []
count = 0
for course in my_rooster.courses:
    for lecture in course.lectures:
        codes.append(lecture.code)
        count += 1
print(count)

# Make a rooster in an array with the lecture codes
room_rooster = make_rooster_random(codes, 4, 5, 7)
print(room_rooster)


def make_rooster_random(codes_list, hours, days, rooms):
    # Make a zeros array with the correct length
    rooster = np.zeros(hours * days * rooms)
    # Get the indices where the lectures will be planned
    slots = random.sample(range(hours * days * rooms), len(codes_list))
    # Put the lecture in the deterimined spot
    for nr, slot in enumerate(slots):
        rooster[slot] = codes_list[nr]
    # Reshape the 1D array to a 3D array for clarity
    return rooster.reshape((rooms, hours, days))


def rooms_dict(file):
    room_dict = {}
    cap_dict = {}
    df = pd.read_csv(file)
    for nr, row in df.iterrows():
        room_dict[nr] = row['Zaalnummber'], row['Max. capaciteit']
        cap_dict[row['Zaalnummber']] = row['Max. capaciteit']
    return room_dict, cap_dict

room_dict, cap_dict = rooms_dict('LecturesLesroosters/zalen.csv')
day_dict = {0: 'ma', 1: 'di', 2: 'wo', 3: 'do', 4: 'vr'}

d = {'student': [], 'vak': [], 'activiteit': [], 'zaal': [], 'dag': [], 'tijdslot': []}
df = pd.read_csv('LecturesLesroosters/studenten_en_vakken2.csv')
for index in np.ndindex(room_rooster.shape):
    if room_rooster[index] != 0:
        for course in my_rooster.courses:
            for lecture in course.lectures:
                if lecture.code == room_rooster[index]:
                    for stud in lecture.studs:
                        d['student'].append(stud)
                        d['vak'].append(course)
                        d['activiteit'].append(lecture.type)
                        d['zaal'].append(room_dict[index[0]][0])
                        d['dag'].append(day_dict[index[2]])
                        d['tijdslot'].append(9 + 2 * index[1])
output = pd.DataFrame(data=d)

def malus_count(df, cap_dict):
    malus = 0
    # Loop over all the students
    for student in df['student'].unique():
        # Get the dagen and tijdsloten of the student
        rooster = df[df['student'] == student].sort_values(by=['dag', 'tijdslot']).loc[:,('dag', 'tijdslot')]
        # Check if there are more than 1 lecture at the same time for this student
        malus += sum(rooster.groupby(['dag', 'tijdslot']).size() - 1)

        # Loop over the days in the students rooster
        for day in rooster['dag'].unique():
            # Get the times of this day
            dag = rooster[rooster['dag'] == day]
            time = dag['tijdslot'].unique()

            # Check if the student has tussenuren
            tussenuur = 0
            if len(time) > 1:
                for timeslot in range(len(time) - 1):
                    # The rooster is not possible if a student has 3 tussenuren
                    if time[timeslot + 1] - time[timeslot] >= 8:
                        print('Not possible')
                    elif time[timeslot + 1] - time[timeslot] == 6:
                        tussenuur += 2
                    elif time[timeslot + 1] - time[timeslot] == 4:
                        tussenuur += 1
            # If the student has 2 tussenuren it is 3 maluspoints and with 1 tussenuur its 1 maluspoint
            if tussenuur == 2:
                malus += 3
            elif tussenuur == 1:
                malus += 1

    # Loop over the different rooms
    for room in df['zaal'].unique():
        # Get expected people of the rooms
        expected = df[df['zaal'] == room].sort_values(by=['tijdslot']).groupby(['dag', 'tijdslot']).size()
        # print(df[df['zaal'] == room])
        # print(room)
        # print(expected)
        for row in expected - cap_dict[room]:
            if row > 0:
                malus += row

    return malus

print(malus_count(output, cap_dict))


#--------------------------------------------------------------------------------------
nr_rooms = 7
nr_timeslots = 4
nr_days = 5

# Availability
# Plan een vak in op basis van availability
# Update availability

availability = np.zeros((nr_timeslots, nr_days))

def check_availability(room_rooster, availability, room):
    """
    Accepts a 3D array of shape nr_rooms x nr_days x nr_timeslots and checks the
    availability for a given room. The function returns a boolean 3D array of
    shape nr_days x nr_timeslots which shows if the timeslot is occupied (False)
    or not (True).
    """
    new_availability = room_rooster[room] == availability
    return new_availability

# Check availability for each room; switch True and False (occupied = 1; not occupied = 0)
for room in range(nr_rooms):
    test = check_availability(room_rooster, availability, room)
    test2 = np.invert(test)
    print(test2 * 5)


# for i in range(nr_lokalen):
#     for j in range(nr_timeslots):
#         for k in range(nr_days):
#             print(room_rooster[i, j, k])

#------------------------------------------------------------------------------------------------------------------------------------------
# class Room():
#     def __init__(self, room_name, room_capacity, timeslot, class_nr):
#         self.name = room_name
#         self.capacity = room_capacity
#         self.timeslot = timeslot # Combination of day and timeslot
#
#
#         # Give the lecture its name, type, lecture code and student numbers
#         d = {'H': 1, 'W': 2, 'P': 3}
#         self.name = lecture_name
#         self.type = lecture_type
#         self.studs = lecture_studs
#         self.code = int(f'{class_nr + 11}{d[lecture_type[0]]}{lecture_type[1]}')
