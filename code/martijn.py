# from classes.rooster import Rooster

# Martijn

import pandas as pd
import math
import random
import numpy as np
from classes.course import Course
from classes.room import Room

class Rooster():
    def __init__(self, courses_df, student_df, rooms_df):
        self.make_courses(courses_df, student_df)
        self.make_rooms(rooms_df)
        self.make_lecture_list()
        self.day_dict = {0: 'ma', 1: 'di', 2: 'wo', 3: 'do', 4: 'vr'}
        self.room_dict = self.make_room_dict(rooms_df)

    def make_room_dict(self, rooms_df):
        room_dict = {}
        for nr, row in rooms_df.iterrows():
            room_dict[nr] = row['Zaalnummber'], row['Max. capaciteit']
        return room_dict

    def make_rooms(self, rooms_df):
        self.rooms = []
        for _, row in rooms_df.iterrows():
            self.rooms.append(Room(4, 5, row['Zaalnummber'], row['Zaalnummber'] == 'C0.110REMOVE', row['Max. capaciteit']))
        self.rooms.sort(key=lambda x: x.capacity, reverse=True)

    def make_courses(self, courses_df, student_df):
        self.courses = []
        # Loop over all the courses needed for the rooster
        for nr, row in courses_df.iterrows():
            course = [row['Vak'], row['#Hoorcolleges'], row['Max. stud. Werkcollege'], row['Max. stud. Practicum']]
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
        hoor_list = []
        for course in self.courses:
            for hoor in course.H:
                hoor_list.append(hoor)
        hoor_list.sort(key=lambda x: x.size, reverse=True)

        wp_list = []
        for course in self.courses:
            for werk in course.W:
                wp_list.append(werk)
        for course in self.courses:
            for prac in course.P:
                wp_list.append(prac)
        wp_list.sort(key=lambda x: x.size, reverse=True)

        self.lectures_list = hoor_list + wp_list

    def make_rooster_random(self, hours, days, rooms):
        # Make a zeros array with the correct length
        self.rooster = np.zeros(hours * days * rooms, dtype=object)
        # Get the indices where the lectures will be planned
        slots = random.sample(range(hours * days * rooms), len(self.lectures_list))
        # Put the lecture in the deterimined spot
        for nr, slot in enumerate(slots):
            self.rooster[slot] = self.lectures_list[nr]
        # Reshape the 1D array to a 3D array for clarity
        self.rooster = self.rooster.reshape((rooms, hours, days))

        for slot in np.ndindex(self.rooster.shape):
            self.rooms[slot[0]].add_course(self.rooster[slot], slot[1:])

    def make_rooster_greedy(self):
        # This can be optimized
        for lecture in self.lectures_list:
            for room in self.rooms:
                if room.capacity > lecture.size and room.availability.any():
                    for slot in np.ndindex(room.rooster.shape):
                        if room.availability[slot]:
                            room.add_course(lecture, slot)
                            break
                    break

    # Not really neccisarry but might still be useful in the future
    def make_output_array(self):
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

    def make_output(self):
        d = {'student': [], 'vak': [], 'activiteit': [], 'zaal': [], 'dag': [], 'tijdslot': []}
        for room in self.rooms:
            for slot in np.ndindex(room.rooster.shape):
                if room.rooster[slot] != 0:
                    lecture = room.rooster[slot]
                    for stud in lecture.studs:
                        d['student'].append(stud)
                        d['vak'].append(lecture.name)
                        d['activiteit'].append(lecture.type)
                        d['zaal'].append(room.room)
                        d['dag'].append(self.day_dict[slot[1]])
                        d['tijdslot'].append(9 + 2 * slot[0])

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
        for room in self.rooms:
            # Get expected people of the rooms
            expected = self.output[self.output['zaal'] == room.room].sort_values(by=['tijdslot']).groupby(['dag', 'tijdslot']).size()
            for row in expected - room.capacity:
                if row > 0:
                    malus += row

        self.malus = malus


courses_df = pd.read_csv('data/vakken.csv')
student_df = pd.read_csv('data/studenten_en_vakken2.csv')
rooms_df = pd.read_csv('data/zalen.csv')

my_rooster = Rooster(courses_df, student_df, rooms_df)
my_rooster.make_rooster_random(4, 5, 7)
my_rooster.make_output()
my_rooster.malus_count()
print(my_rooster.malus)
# for room in my_rooster.rooms:
#     print(room.capacity)
# for lec in my_rooster.lectures_list:
#     print(lec.size, lec.type)
# print(my_rooster.rooster)
# for room in my_rooster.rooms:
#     print(room.rooster)
#     print(room.room)
#     print(room.availability)
# print(my_rooster.output)
my_rooster.output.to_csv('data/random_rooster.csv')


my_rooster2 = Rooster(courses_df, student_df, rooms_df)
my_rooster2.make_rooster_greedy()
my_rooster2.make_output()
my_rooster2.malus_count()
print(my_rooster2.malus)
my_rooster2.output.to_csv('data/greedy_rooster.csv')
# for room in my_rooster2.rooms:
#     print(room.rooster.shape)
# print(my_rooster2.output)
