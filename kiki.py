# Kiki
import pandas as pd
import math
import random
import numpy as np
from classes.course import Course
from classes.room import Room
from classes.lecture import Lecture
import yaml
import pdfschedule

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
                if room.capacity > lecture.size and np.any(room.rooster==0):
                    # Loop over the indices where the room rooster is 0
                    for slot in list(zip(*np.nonzero(room.rooster==0))):
                        room.add_course(lecture, slot)
                        break
                    break

    def hillclimber(self):
        for nr3, lecture1 in enumerate(self.lectures_list):
            for nr1, room1 in enumerate(self.rooms):
                for slot1 in np.ndindex(room1.rooster.shape):
                    if lecture1 == room1.rooster[slot1]:
                        tries = {}
                        self.malus_count()
                        for nr2, room2 in enumerate(self.rooms):
                            for slot2 in np.ndindex(room2.rooster.shape):
                                lecture2 = room2.rooster[slot2]
                                room1.add_course(lecture2, slot1)
                                room2.add_course(lecture1, slot2)
                                self.malus_count()
                                tries[(nr1, slot1), (nr2, slot2)] = sum(self.malus)
                                room1.add_course(lecture1, slot1)
                                room2.add_course(lecture2, slot2)

                        slot = [k for k, v in tries.items() if v==min(tries.values())][0]
                        self.rooms[slot[0][0]].add_course(self.rooms[slot[1][0]].rooster[slot[1][1]], slot[0][1])
                        self.rooms[slot[1][0]].add_course(lecture1, slot[1][1])

    def simulated_annealing(self, alpha=0.01):
        temperature = 50
        for nr3, lecture1 in enumerate(self.lectures_list):
            for nr1, room1 in enumerate(self.rooms):
                for slot1 in np.ndindex(room1.rooster.shape):
                    if lecture1 == room1.rooster[slot1]:
                        acceptance_count = 0

                        for nr2, room2 in enumerate(self.rooms):
                            for slot2 in np.ndindex(room2.rooster.shape):
                                self.malus_count()
                                old = sum(self.malus)
                                lecture2 = room2.rooster[slot2]
                                room1.add_course(lecture2, slot1)
                                room2.add_course(lecture1, slot2)
                                self.malus_count()
                                new = sum(self.malus)
                                acceptance = 2 ** ((old - new) / temperature)
                                temperature -= alpha

                                if random.uniform(0, 1) > acceptance:
                                    room1.add_course(lecture1, slot1)
                                    room2.add_course(lecture2, slot2)

                                elif acceptance == 1:
                                    acceptance_count += 1
                                    print(acceptance_count)

                            if acceptance_count == 10:
                                break

    def make_output(self):
        '''
        Makes a DataFrame with the required columns for the malus_count function
        '''
        # Empty dictionary to store all the information
        d = {'student': [], 'dag': [], 'tijdslot': []}

        for room in self.rooms:
            # Go over every timeslot for this room
            for slot in np.ndindex(room.rooster.shape):
                # Check if there is a lecture
                if room.rooster[slot] != 0:
                    lecture = room.rooster[slot]
                    # Add all the students for this lecture into the dictionary
                    for stud in lecture.studs:
                        d['student'].append(stud)
                        d['dag'].append(slot[1])
                        d['tijdslot'].append(slot[0])

        # Make a DataFrame from the dictionary
        self.output = pd.DataFrame(data=d)

    def make_csv(self, filename):
        '''
        Makes a DataFrame with the required columns for the output and saves it to a csv-file
        '''
        # Mapping dictionaries
        day_dict = {0: 'ma', 1: 'di', 2: 'wo', 3: 'do', 4: 'vr'}
        time_dict = {0: 9, 1: 11, 2: 13, 3: 15, 4: 17}

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
                        d['dag'].append(day_dict[slot[1]])
                        d['tijdslot'].append(time_dict[slot[0]])

        # Save the DataFrame as csv with the given filename/path
        pd.DataFrame(data=d).to_csv(filename)


    def make_scheme(self):
        dict = {'name': [], 'days': [], 'time': []}
        day_dict_scheme = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri'}
        for room in self.rooms:
            for slot in np.ndindex(room.rooster.shape):
                if room.rooster[slot] != 0:
                    lecture = room.rooster[slot]
                    dict['name'].append(f'{lecture.name}, type: {lecture.type}, size: {lecture.size}')
                    dict['days'].append(day_dict_scheme[slot[1]])
                    dict['time'].append(f'{9 + 2 * slot[0]} - {+ 11 + 2 * slot[0]}')

                    df = pd.DataFrame(data=dict)

                    with open(f'../data/room{room.room}.yaml', 'w') as file:
                        documents = yaml.dump(df.to_dict(orient='records'), file, default_flow_style=False)

    def malus_count(self):
        '''
        Counts the amount of malus points from the output DataFrame
        '''
        # Different maluspoint counters
        double_hours = 0
        tussenuren = 0
        avondsloten = 0
        small_room = 0

        # Removes the groups with only 1 row to go even faster
        groups = self.output.loc[self.output.groupby(['student', 'dag'])['tijdslot'].transform('count') > 1, :]

        # Get the lectures for each student per day
        for _, day in groups.groupby(['student', 'dag'])['tijdslot']:
            # Count how often a timeslot occurs for a student per day
            count = {}
            for slot in day:
                if slot in count:
                    count[slot] += 1
                else:
                    count[slot] = 1
            # Get the correct amount of malus points from the dictionary
            double_hours += sum(count.values()) - len(count)
            # Get the time slots from the dictionary
            slots = list(count.keys())
            # Check if the student more than 1 lecture this day
            if len(slots) > 1:
                tussenuur = 0
                slots.sort()
                # Loop over the 2 consecutive lectures
                for slot in range(1, len(slots)):
                    # See how many timeslots were skipped and do the correct thing
                    dif = slots[slot] - slots[slot - 1]
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

courses_df = pd.read_csv('../data/vakken.csv')
student_df = pd.read_csv('../data/studenten_en_vakken2.csv')
rooms_df = pd.read_csv('../data/zalen.csv')

evenings = {}
my_rooster = Rooster(courses_df, student_df, rooms_df, evenings)
my_rooster.make_rooster_random(4, 5, 7)
my_rooster.make_output()
my_rooster.make_scheme()
my_rooster.malus_count()
