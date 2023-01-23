import pandas as pd
import math
import random
import numpy as np
import yaml
import pdfschedule
from .course import Course
from .room import Room
from .student import Student

class Rooster():
    def __init__(self, courses_df, student_df, rooms_df, evenings):
        # Initialize all the required variables
        self.make_student_dict(courses_df, student_df)
        self.make_rooms(rooms_df, evenings)
        self.make_courses(courses_df)
        self.make_lecture_list()

    def make_student_dict(self, courses_df, student_df):
        '''
        Makes a list of students and a dictionary of students per course
        '''
        # Initialize a list for all the student objects
        self.student_list = []
        # Fill the student_list with student objects
        for _, student in student_df.iterrows():
            self.student_list.append(Student(student['Stud.Nr.'], 5, 5, student['Vakken']))

        # Initialize a dictionary for lists of student objects per course
        self.student_dict = {}
        # Loop over every course
        for _, course in courses_df.iterrows():
            self.student_dict[course['Vak']] = []
            # Check for every student if they are in this course
            for student in self.student_list:
                if course['Vak'] in student.courses:
                    self.student_dict[course['Vak']].append(student)

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

    def make_courses(self, courses_df):
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
            # Make the course class with the students for the course
            self.courses.append(Course(course, self.student_dict[course[0]], nr))

    def make_lecture_list(self):
        '''
        Makes a list of lecture objects with first all the hoorcolleges sorted on size
        and then the tutorials and practicals sorted on size
        '''
        hoor_list = []
        wp_list = []

        # Put all the hoorcolleges in a list
        for course in self.courses:
            for hoor in course.H:
                hoor_list.append(hoor)

        # Put all the tutorials and practicals in a list
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
        Makes a random rooster (without any eveningslots) by
        placing each lecture in a random room, day and timeslot
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
            if self.rooster[slot] != 0:
                self.rooms[slot[0]].swap_course(0, self.rooster[slot], slot[1:])

    def make_rooster_greedy(self):
        '''
        Makes a rooster bases on the first spot that a lecture can fit in by
        comparing lecture size and room capacity
        '''
        # Check for each lecture the first possible slot to put it in, only places a lecture once
        for lecture in self.lectures_list:
            for room in self.rooms:
                # Check if the lecture fits and if there is a slot without a lecture
                if room.capacity >= lecture.size and np.any(room.rooster==0):
                    # Get the first slot where the room is still empty and put the lecture there
                    room.swap_course(0, lecture, list(zip(*np.nonzero(room.rooster==0)))[0])
                    break

    def make_rooster_minmalus(self):
        '''
        Puts the biggest 10 lectures randomly in the biggest room for 11 till 15,
        this causes no malus points. After that it loops over the remaining lectures
        and puts them randomly in one of the slots which causes the least amount
        of malus points, without thinking about the remaining lectures.
        '''
        # Put the biggest 10 lectures randomly in the biggest room for 11 till 15
        start_lectures = random.sample(self.lectures_list[:10], 10)
        for nr, slot in enumerate(np.ndindex(2, 5)):
            self.rooms[0].swap_course(0, start_lectures[nr], (slot[0] + 1, slot[1]))

        # Loop over the remaining lectures
        for lecture in self.lectures_list[10:]:
            # Make a dictionary to track the malus points for each slot
            tries = {}
            # Loop over all the empty slots in each room
            for nr, room in enumerate(self.rooms):
                for slot in list(zip(*np.nonzero(room.rooster==0))):
                    # Add lecture in this slot, get the new malus and put it in the dict and remove lecture again
                    room.swap_course(0, lecture, slot)
                    self.malus_count()
                    tries[nr, (slot)] = sum(self.malus)
                    room.swap_course(lecture, 0, slot)

            # Randomly get one of the slots with the least malus points
            slot = random.choice([k for k, v in tries.items() if v==min(tries.values())])
            # Add the lecture to this room and slot
            self.rooms[slot[0]].swap_course(0, lecture, slot[1])

            # Get the updated malus count and print useful info
            self.malus_count()
            print(lecture.code, self.malus, sum(self.malus), lecture.size)

    def hillclimber_activities(self):
        '''
        Does one loop over all the lectures and finds the best fit for each of them
        by swapping with all other possibilities (lectures or empty slots)
        '''
        # Loop over all the lectures randomly
        for nr3, lecture1 in enumerate(random.sample(self.lectures_list, len(self.lectures_list))):
            # Get the room and slot where this lecture is place now
            room1 = lecture1.room
            slot1 = lecture1.slot
            # Make a dictionary to track the malus points for each slot
            tries = {}
            # Loop over all the slots in each room
            for nr2, room2 in enumerate(self.rooms):
                for slot2 in np.ndindex(room2.rooster.shape):
                    # Get which lecture is placed in this room and slot
                    lecture2 = room2.rooster[slot2]
                    # Swap these 2 lectures, get the new malus and put it in the dict and swap them back
                    self.swap_course(room1, lecture1, slot1, room2, lecture2, slot2)
                    self.malus_count()
                    tries[nr2, slot2] = sum(self.malus)
                    self.swap_course(room1, lecture2, slot1, room2, lecture1, slot2)

            # Randomly get one of the slots with the least malus points
            slot = random.choice([k for k, v in tries.items() if v==min(tries.values())])

            # Get which room and lecture need to be switched and swap them
            room2 = self.rooms[slot[0]]
            lecture2 = room2.rooster[slot[1]]
            self.swap_course(room1, lecture1, slot1, room2, lecture2, slot[1])

            # Get the updated malus count and print useful info
            self.malus_count()
            print(lecture1.code, self.malus, sum(self.malus), nr3)

    def swap_course(self, room1, lec1, slot1, room2, lec2, slot2):
        '''
        Swaps 2 lectures from room and slot and updates the corresponding student roosters
        '''
        # Swap the 2 lectures in the room roosters
        room1.rooster[slot1] = lec2
        room2.rooster[slot2] = lec1

        # Check if it is a lecture and not an empty slot
        if lec1 != 0:
            # Update the lecture attributes
            lec1.room = room2
            lec1.slot = slot2
            # Update all the roosters for the students with this lecture
            for stud in lec1.studs:
                stud.swap_lecture(lec1, slot1, lec1, slot2)

        # Check if it is a lecture and not an empty slot
        if lec2 != 0:
            # Update the lecture attributes
            lec2.room = room1
            lec2.slot = slot1
            # Update all the roosters for the students with this lecture
            for stud in lec2.studs:
                stud.swap_lecture(lec2, slot2, lec2, slot1)

        # Update the malus counts for both rooms
        room1.update_malus()
        room2.update_malus()

    def move_student(self, student, lec1, slot1, lec2, slot2):
        '''
        Removes a student from a lecture and adds it to another one.
        Also updates the student rooster and malus points
        '''
        lec1.studs.remove(student)
        lec1.size -= 1
        lec1.room.update_malus()
        lec2.studs.append(student)
        lec2.size += 1
        lec2.room.update_malus()
        # Remove lec1 and add lec2 to student rooster
        student.swap_lecture(lec1, slot1, lec2, slot2)

    def swap_student(self, student1, lec1, slot1, student2, lec2, slot2):
        '''
        Removes a student from a lecture and adds it to another one.
        Also updates the student rooster and malus points
        '''
        lec1.studs.remove(student1)
        lec2.studs.append(student1)
        lec2.studs.remove(student2)
        lec1.studs.append(student2)

        # Remove lec1 and add lec2 to student rooster
        student1.swap_lecture(lec1, slot1, lec2, slot2)
        student2.swap_lecture(lec2, slot2, lec1, slot1)

    def hillclimber_students(self, werk_or_prac):
        """
        Moves students in werkgroep or practicumgroep, based on a decreasing
        number of malus points.
        """
        for nr, course in enumerate(self.courses): # Ga alle vakken langs
            nr_werk_groups = len(getattr(course, werk_or_prac))

            for group in getattr(course, werk_or_prac):
                group_nr = int(group.type[1])

                for student in group.studs:
                    tries = {} # key = group nr, value = malus
                    tries2 = {} # key = list of group nr and student index; value = malus
                    self.malus_count()
                    tries[group_nr] = sum(self.malus)
                    tries2[student] = sum(self.malus)

                    for i in range(nr_werk_groups):
                        new_group_nr = i + 1
                        new_group = getattr(course, werk_or_prac)[i]

                        if new_group_nr != group_nr and new_group.max_studs > new_group.size: # Houd rekening met maximale aantal studenten per werkgroep
                            self.move_student(student, group, group.slot, new_group, new_group.slot)
                            self.malus_count() # Maluspunten voor eventuele nieuwe groep
                            tries[new_group_nr] = sum(self.malus)
                            self.move_student(student, new_group, new_group.slot, group, group.slot)

                        if new_group_nr != group_nr:
                            for nr1, other_student in enumerate(new_group.studs):
                                self.swap_student(student, group, group.slot, other_student, new_group, new_group.slot)
                                self.malus_count()
                                tries2[(new_group_nr, other_student)] = sum(self.malus)
                                self.swap_student(other_student, group, group.slot, student, new_group, new_group.slot)

                    best_move_nr = random.choice([k for k, v in tries.items() if v==min(tries.values())]) # Select group in which the student can best be placed
                    move_malus = tries[best_move_nr]
                    best_move = getattr(course, werk_or_prac)[best_move_nr - 1]

                    best_swap_try = random.choice([k for k, v in tries2.items() if v==min(tries2.values())]) # Select group in which the student can best be placed

                    # Als de originele maluscount (met key = studentnummer) niet de laagste is bij swappen
                    if best_swap_try != student:
                        best_swap_nr = best_swap_try[0] # Correct group to swap the student to
                        best_swap_stud = best_swap_try[1] # Index to search the right student
                        swap_malus = tries2[best_swap_try]
                        best_swap = getattr(course, werk_or_prac)[best_swap_nr - 1]

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

            self.malus_count()
            print(self.malus, sum(self.malus), nr, werk_or_prac)


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
        day_dict_scheme = {0: 'M', 1: 'T', 2: 'W', 3: 'R', 4: 'F'}
        for room in self.rooms:
            dict = {'name': [], 'days': [], 'time': []}
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
        Calculates the total malus points for the rooster by summing over all the
        students and rooms
        '''
        # Start counting from 0
        self.malus = [0, 0, 0, 0]
        # Add all the malus points from students
        for student in self.student_list:
            self.malus[0] += student.malus[0]
            self.malus[1] += student.malus[1]
        # Add all the malus points from rooms
        for room in self.rooms:
            self.malus[2] += room.malus[0]
            self.malus[3] += room.malus[1]
