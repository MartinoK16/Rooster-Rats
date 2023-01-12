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
        self.size = len(lecture_studs)
        # print(self.code)
        # print(self.name)
        # print(self.type)
        # print(self.studs)

class Course():
    def __init__(self, course, student_list, class_nr):
        # Give for every course its name, #hoor, max studs werk, max studs prac and the student list for this course
        self.name = course[0]
        self.nr = class_nr
        self.students = random.sample(student_list, len(student_list))
        self.size = len(self.students)
        self.H = []
        self.W = []
        self.P = []

        for nr in range(course[1]):
            self.H.append(Lecture(self.name, f'H{nr + 1}', self.students, self.nr))

        if course[2] > 0:
            self.add_werk(course[2])
        if course[3] > 0:
            self.add_werk(course[3])

    def add_werk(self, max_studs):
        slices = self.make_slices(max_studs)
        for nr in range(len(slices) - 1):
            self.W.append(Lecture(self.name, f'W{nr + 1}', self.students[slices[nr]:slices[nr + 1]], self.nr))

    def add_prac(self, nr_studs, max_studs):
        slices = self.make_slices(max_studs)
        for nr in range(len(slices) - 1):
            self.P.append(Lecture(self.name, f'P{nr + 1}', self.students[slices[nr]:slices[nr + 1]], self.nr))

    def make_slices(self, max_studs):
        rooms = math.ceil(self.size / max_studs)
        min_stud = self.size // rooms
        extra_stud = self.size % rooms

        groups = []
        for nr, room in enumerate(range(rooms)):
            groups.append(min_stud)
            if nr < extra_stud:
                groups[nr] += 1

        slices = [0]
        for nr, group in enumerate(groups):
            slices.append(group + slices[nr])

        return slices


                    # # Nr of werkcolleges and groups of students per werkcollege and make a lecture of it
                    # rooms = 0
                    # if self.werk > 0:
                    #     rooms = math.ceil(len(self.students) / self.werk)
                    # for nr in range(rooms):
                    #     nr_students = len(self.students) // rooms
                    #     self.lectures.append(Lecture(self.name, f'W{nr + 1}', self.students[nr * nr_students:(nr + 1) * nr_students], class_nr))
                    #
                    # # Nr of practica and groups of students per practica and make a lecture of it
                    # rooms = 0
                    # if self.prac > 0:
                    #     rooms = math.ceil(len(self.students) / self.prac)
                    # for nr in range(rooms):
                    #     nr_students = len(self.students) // rooms
                    #     self.lectures.append(Lecture(self.name, f'P{nr + 1}', self.students[nr * nr_students:(nr + 1) * nr_students], class_nr))


class Rooster():
    def __init__(self, courses_df, student_df, rooms_df):
        self.courses_list = self.make_courses_list(courses_df)
        self.courses = []
        self.make_courses(self.courses_list, student_df)
        self.lectures_list = self.make_lecture_list()
        self.day_dict = {0: 'ma', 1: 'di', 2: 'wo', 3: 'do', 4: 'vr'}
        self.room_dict, self.cap_dict = self.make_room_dict(rooms_df)

    def make_room_dict(self, rooms_df):
        room_dict = {}
        cap_dict = {}
        for nr, row in rooms_df.iterrows():
            room_dict[nr] = row['Zaalnummber'], row['Max. capaciteit']
            cap_dict[row['Zaalnummber']] = row['Max. capaciteit']
        return room_dict, cap_dict

    def make_courses_list(self, df):
        courses_list = []
        for _, row in df.iterrows():
            courses_list.append([row['Vak'], row['#Hoorcolleges'], row['Max. stud. Werkcollege'], row['Max. stud. Practicum']])
        return courses_list

    def make_courses(self, courses_list, student_df):
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

    def make_lecture_list(self):
        lectures = []
        for course in self.courses:
            for hoor in course.H:
                lectures.append(hoor)
        for course in self.courses:
            for werk in course.W:
                lectures.append(werk)
        for course in self.courses:
            for prac in course.P:
                lectures.append(prac)

        return lectures

    def make_rooster_random(self, hours, days, rooms):
        # Make a zeros array with the correct length
        rooster = np.zeros(hours * days * rooms, dtype=object)
        # Get the indices where the lectures will be planned
        slots = random.sample(range(hours * days * rooms), len(self.lectures_list))
        # Put the lecture in the deterimined spot
        for nr, slot in enumerate(slots):
            rooster[slot] = self.lectures_list[nr]
        # Reshape the 1D array to a 3D array for clarity
        self.rooster = rooster.reshape((rooms, hours, days))

    def make_output(self):
        d = {'student': [], 'vak': [], 'activiteit': [], 'zaal': [], 'dag': [], 'tijdslot': []}
        for index in np.ndindex(self.rooster.shape):
            if self.rooster[index] != 0:
                lecture = self.rooster[index]
                for stud in self.rooster[index].studs:
                    d['student'].append(stud)
                    d['vak'].append(lecture.name)
                    d['activiteit'].append(lecture.type)
                    d['zaal'].append(self.room_dict[index[0]][0])
                    d['dag'].append(self.day_dict[index[2]])
                    d['tijdslot'].append(9 + 2 * index[1])

        self.output = pd.DataFrame(data=d)

    def malus_count(self):
        malus = 0
        # Loop over all the students
        for student in self.output['student'].unique():
            # Get the dagen and tijdsloten of the student
            rooster = self.output[self.output['student'] == student].sort_values(by=['dag', 'tijdslot']).loc[:,('dag', 'tijdslot')]
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
        for room in self.output['zaal'].unique():
            # Get expected people of the rooms
            expected = self.output[self.output['zaal'] == room].sort_values(by=['tijdslot']).groupby(['dag', 'tijdslot']).size()
            for row in expected - self.cap_dict[room]:
                if row > 0:
                    malus += row

        self.malus = malus


# Returns a list with Name, #Hoorcolleges, Max Stud Werkcollege, Max Stud Practicum
courses_df = pd.read_csv('LecturesLesroosters/vakken.csv')
student_df = pd.read_csv('LecturesLesroosters/studenten_en_vakken2.csv')
rooms_df = pd.read_csv('LecturesLesroosters/zalen.csv')

# Make a Rooster object with the courses and students DataFrame
my_rooster = Rooster(courses_df, student_df, rooms_df)
my_rooster.make_rooster_random(4, 5, 7)
print(my_rooster.rooster)
my_rooster.make_output()
print(my_rooster.output)
my_rooster.output.to_csv('LecturesLesroosters/test.csv')  
my_rooster.malus_count()
print(my_rooster.malus)






#print(malus_count(output, cap_dict))


#--------------------------------------------------------------------------------------
nr_rooms = 7
nr_timeslots = 4
nr_days = 5

# Availability
# Plan een vak in op basis van availability
# Update availability


# for i in range(nr_lokalen):
#     for j in range(nr_timeslots):
#         for k in range(nr_days):
#             print(room_rooster[i, j, k])

# ------------------------------------------------------------------------------------------------------------------------------------------
class Room():
    def __init__(self, nr_timeslots, nr_days, room, evening, room_capacity, day, timeslot, course):
        self.nr_timeslots = nr_timeslots # Standard; without evening timeslot
        self.nr_days = nr_days
        self.room = room
        self.evening = evening # Boolean
        self.capacity = room_capacity

        # Wat moet je hiermee?
        self.day = day
        self.timeslot = timeslot
        self.course = course

        # Create first version of rooster and availability
        if self.evening:
            self.availability = np.zeros((nr_timeslots + 1, nr_days))
            self.rooster = np.zeros((nr_timeslots + 1, nr_days))
        else:
            self.availability = np.zeros((nr_timeslots, nr_days))
            self.rooster = np.zeros((nr_timeslots, nr_days))

    def check_availability(self):
        """
        Accepts a 3D array of shape nr_rooms x nr_days x nr_timeslots and checks
        the availability for a given room. The function returns a boolean 3D
        array of shape nr_days x nr_timeslots which shows if the timeslot is
        occupied (True) or not (False).
        """
        # Check availability for the room; switch True and False (occupied = 1;
        # not occupied = 0)
        self.availability = np.invert(self.rooster[self.room] == self.availability)

    def remove_course(self, timeslot):
        self.rooster[day, timeslot] = 0
        # Ook availability updaten naar 0?

    def add_course(self, timeslot):
        self.rooster[day, timeslot] = self.course
        # Ook availability updaten naar 1?

output_df = pd.read_csv('LecturesLesroosters/test.csv')

# Loop over the different rooms
for student in output_df['student'].unique():
    # Get expected people of the rooms
    expected = output_df[output_df['student'] == student]
    print(expected)
