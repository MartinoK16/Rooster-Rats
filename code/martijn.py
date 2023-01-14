# from classes.rooster import Rooster

# Martijn

import pandas as pd
import math
import random
import numpy as np
from classes.course import Course
from classes.room import Room
import copy
import time

class Rooster():
    def __init__(self, courses_df, student_df, rooms_df, evenings):
        # Make the required classes and list
        self.make_rooms(rooms_df, evenings)
        self.make_courses(courses_df, student_df)
        self.make_lecture_list()

    def make_rooms(self, rooms_df, evenings):
        '''
        Makes a list of room objects based on a DataFrame and sorts them by room capacity
        '''
        self.rooms = []
        # Make the room class for each room from the DataFrame
        for _, row in rooms_df.iterrows():
            self.rooms.append(Room(4, 5, row['Zaalnummber'], row['Zaalnummber'] in evenings, row['Max. capaciteit']))

        # Sort the rooms based on capacity
        self.rooms.sort(key=lambda x: x.capacity, reverse=True)

    def make_courses(self, courses_df, student_df):
        '''
        Makes a list of course objects based on a DataFrame and the students which have that course
        '''
        self.courses = []
        # Loop over the courses in the DataFrame
        for nr, row in courses_df.iterrows():
            # Get the required information for this course
            course = [row['Vak'], row['#Hoorcolleges'], row['Max. stud. Werkcollege'], row['Max. stud. Practicum']]
            # Replace NaNs with 0
            course[1:] = [0 if math.isnan(i) else i for i in course[1:]]

            # Go over all the students to see who have this course
            student_list = []
            for _, student in student_df.iterrows():
                if course[0] in student['Vakken']:
                    student_list.append(student['Stud.Nr.'])

            # Make the course class with the students
            self.courses.append(Course(course, student_list, nr))

    def make_lecture_list(self):
        '''
        Makes a list of lecture objects based on the course objects and sorts is based on lecture type and size
        '''
        hoor_list = []
        wp_list = []

        # Put all the Hoorcolleges in a list
        for course in self.courses:
            for hoor in course.H:
                hoor_list.append(hoor)

        # Put all the Werkcolleges and Practica in a list
        for course in self.courses:
            for werk in course.W:
                wp_list.append(werk)
            for prac in course.P:
                wp_list.append(prac)

        # Sort the list based on the lecture size
        hoor_list.sort(key=lambda x: x.size, reverse=True)
        wp_list.sort(key=lambda x: x.size, reverse=True)

        # Add the 2 sorted lists together
        self.lectures_list = hoor_list + wp_list

    def make_rooster_random(self, hours, days, rooms):
        '''
        Makes a random rooster (without any eveningslots) by placing each lecture in a random room, day and time
        '''
        # Make a zeros array with the correct length
        self.rooster = np.zeros(hours * days * rooms, dtype=object)
        # Get the indices where the lectures will be planned randomly
        slots = random.sample(range(hours * days * rooms), len(self.lectures_list))

        # Put the lecture in the deterimined spot
        for nr, slot in enumerate(slots):
            self.rooster[slot] = self.lectures_list[nr]

        # Reshape the 1D array to a 3D array for easy use
        self.rooster = self.rooster.reshape((rooms, hours, days))

        # Add the arrays into the rooms classes roosters
        for slot in np.ndindex(self.rooster.shape):
            self.rooms[slot[0]].add_course(self.rooster[slot], slot[1:])

    def make_rooster_greedy(self):
        '''
        Makes a rooster bases on the first spot that a lecture can fit in by comparing lecture size and room capacity
        '''
        # Check for each lecture the first possible slot to put it in, only places a lecture once
        for lecture in self.lectures_list:
            for room in self.rooms:
                if room.capacity > lecture.size and room.availability.any():
                    for slot in np.ndindex(room.rooster.shape):
                        if room.availability[slot]:
                            room.add_course(lecture, slot)
                            break
                    break

    def make_output(self):
        '''
        Makes a DataFrame with the required columns for the malus_count function
        '''
        # Empty dictionary to store all the information
        d = {'student': [], 'vak': [], 'activiteit': [], 'zaal': [], 'dag': [], 'tijdslot': []}

        for room in self.rooms:
            # Go over every timeslot for this room
            for slot in np.ndindex(room.rooster.shape):
                # Check if there is a lecture
                if room.rooster[slot] != 0:
                    lecture = room.rooster[slot]
                    # Add all the students for this lecture into the dictionary
                    for stud in lecture.studs:
                        d['student'].append(stud)
                        d['vak'].append(lecture.name)
                        d['activiteit'].append(lecture.type)
                        d['zaal'].append(room.room)
                        d['dag'].append(slot[1])
                        d['tijdslot'].append(slot[0])

        # Make a DataFrame from the dictionary
        self.output = pd.DataFrame(data=d)

    def make_csv(self, filename):
        '''
        Changes the format of the dag and tijdslot columns before making a csv-file from the output DataFrame
        '''
        # Mapping dictionaries
        day_dict = {0: 'ma', 1: 'di', 2: 'wo', 3: 'do', 4: 'vr'}
        time_dict = {0: 9, 1: 11, 2: 13, 3: 15, 4: 17}

        # Make a copy of the output DataFrame and change the dag and tijdslot columns
        file = copy.copy(self.output)
        file['dag'] = file['dag'].map(day_dict)
        file['tijdslot'] = file['tijdslot'].map(time_dict)

        # Save the DataFrame as csv with the given filename/path
        file.to_csv(filename)

    def malus_count(self):
        '''
        Counts the amount of malus points from the output DataFrame
        '''
        st = time.time()
        # Different maluspoint counters
        double_hours = 0
        tussenuren = 0
        avondsloten = 0
        small_room = 0

        # Get the lectures for each student
        for _, student in self.output.groupby('student')[['dag', 'tijdslot']]:
            # Check if a student has more than one lecture at the same time
            double_hours += sum(student.groupby(['dag', 'tijdslot']).size() - 1)

            # Loop over the days in the students rooster
            for _, day in student.groupby('dag'):
                # Get the times of this day
                slots = day['tijdslot'].unique()

                # Check if the student more than 1 lecture this day
                if len(slots) > 1:
                    tussenuur = 0
                    slots.sort()

                    # Loop over the 2 consecutive lectures
                    for slot in range(len(slots) - 1):
                        # See how many timeslots were skipped and do the correct thing
                        dif = slots[slot + 1] - slots[slot]

                        if dif == 1:
                            pass
                        elif dif == 2:
                            tussenuur += 1
                        elif dif == 3:
                            tussenuur += 2
                        elif dif == 4:
                            # The rooster is not possible if a student has 3 tussenuren
                            print('Not possible')
                            tussenuren += 10000

                    # If the student has 1 tussenuur it's 1 maluspoint and with 3 tussenuren it's 3 maluspoints
                    if tussenuur == 1:
                        tussenuren += 1
                    elif tussenuur == 2:
                        tussenuren += 3

        # Check if any evening slots are used and give 5 point for each use
        for room in self.rooms:
            if room.evening:
                for avondslot in room.rooster[4, :]:
                    if avondslot != 0:
                        avondsloten += 5

        # Check if rooms are overfull
        # Shouldn't be neccisarry if the rooster is made to only put lectures in rooms where they fit
        for room in self.rooms:
            for slot in np.ndindex(room.rooster.shape):
                if room.rooster[slot] != 0:
                    small_room += max(room.rooster[slot].size - room.capacity, 0)

        # Add up all the malus points for the total
        self.malus = double_hours + tussenuren + avondsloten + small_room

        et = time.time()

        # get the execution time
        elapsed_time = et - st
        print('Execution time:', elapsed_time, 'seconds')


courses_df = pd.read_csv('../data/vakken.csv')
student_df = pd.read_csv('../data/studenten_en_vakken2.csv')
rooms_df = pd.read_csv('../data/zalen.csv')
evenings = {'C0.110REMOVE'}

my_rooster = Rooster(courses_df, student_df, rooms_df, evenings)
my_rooster.make_rooster_random(4, 5, 7)
my_rooster.make_output()
my_rooster.malus_count()
print(my_rooster.malus)
# my_rooster.malus_count_old()
# print(my_rooster.malus)

my_rooster2 = Rooster(courses_df, student_df, rooms_df, evenings)
my_rooster2.make_rooster_greedy()
my_rooster2.make_output()
my_rooster2.malus_count()
print(my_rooster2.malus)
# my_rooster2.malus_count_old()
# print(my_rooster2.malus)
# my_rooster2.make_csv('../data/test123.csv')
