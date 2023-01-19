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
        # Make the required classes and list
        self.make_student_dict(courses_df, student_df)
        self.make_rooms(rooms_df, evenings)
        self.make_courses(courses_df)
        self.make_lecture_list()

    def make_student_dict(self, courses_df, student_df):
        self.student_dict = {}
        self.student_list = []

        for _, student in student_df.iterrows():
            self.student_list.append(Student(student['Stud.Nr.'], 5, 5, student['Vakken']))

        for _, course in courses_df.iterrows():
            self.student_dict[course['Vak']] = []

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
            # Make the course class with the students
            self.courses.append(Course(course, self.student_dict[course[0]], nr))

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
        # self.lectures_list.sort(key=lambda x: x.size, reverse=True)

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
            if self.rooster[slot] != 0:
                self.rooms[slot[0]].add_course(self.rooster[slot], slot[1:])

    def make_rooster_greedy(self):
        '''
        Makes a rooster bases on the first spot that a lecture can fit in by comparing lecture size and room capacity
        '''
        # Check for each lecture the first possible slot to put it in, only places a lecture once
        for lecture in self.lectures_list:
            for room in self.rooms:
                if room.capacity >= lecture.size and np.any(room.rooster==0):
                    # Loop over the indices where the room rooster is 0
                    room.add_course(lecture, list(zip(*np.nonzero(room.rooster==0)))[0])
                    break

    def make_rooster_minmalus(self):
        # Randomly samples the first 10 lectures
        start_lectures = random.sample(self.lectures_list[:10], 10)
        for nr, slot in enumerate(np.ndindex(2, 5)):

            # Add lecture class to first and biggest room class
            self.rooms[0].add_course(start_lectures[nr], (slot[0] + 1, slot[1]))

        # Check for each lecture the first possible slot to put it in, only places a lecture once
        for lecture in self.lectures_list: # [10:]
            tries = {}
            for nr, room in enumerate(self.rooms):
                if np.any(room.rooster==0): # room.capacity >= lecture.size and
                    # Loop over the indices where the room rooster is 0
                    for slot in list(zip(*np.nonzero(room.rooster==0))):
                        room.add_course(lecture, slot)
                        self.malus_count()
                        tries[nr, slot[0], slot[1]] = sum(self.malus)
                        room.remove_course(lecture, slot)

            slot = random.choice([k for k, v in tries.items() if v==min(tries.values())])
            self.rooms[slot[0]].add_course(lecture, slot[1:])
            self.malus_count()

    def hillclimber(self):
        for nr3, lecture1 in enumerate(random.sample(self.lectures_list, len(self.lectures_list))):
            for nr1, room1 in enumerate(self.rooms):
                for slot1 in np.ndindex(room1.rooster.shape):
                    if room1.rooster[slot1] != 0:
                        if lecture1.code == room1.rooster[slot1].code:
                            tries = {}
                            self.malus_count()
                            tries[(nr1, slot1), (nr1, slot1)] = sum(self.malus)
                            print(lecture1.code, self.malus, sum(self.malus), nr3)
                            for nr2, room2 in enumerate(self.rooms):
                                for slot2 in np.ndindex(room2.rooster.shape):
                                    lecture2 = room2.rooster[slot2]
                                    if lecture1 != lecture2:
                                        room1.rem_course(lecture1, slot1)
                                        room2.rem_course(lecture2, slot2)
                                        room1.add_course(lecture2, slot1)
                                        room2.add_course(lecture1, slot2)
                                        self.malus_count()
                                        tries[(nr1, slot1), (nr2, slot2)] = sum(self.malus)
                                        room1.rem_course(lecture2, slot1)
                                        room2.rem_course(lecture1, slot2)
                                        room1.add_course(lecture1, slot1)
                                        room2.add_course(lecture2, slot2)

                            slot = random.choice([k for k, v in tries.items() if v==min(tries.values())])
                            if slot != ((nr1, slot1), (nr1, slot1)):
                                lecture2 = self.rooms[slot[1][0]].rooster[slot[1][1]]
                                room1.rem_course(lecture1, slot[0][1])
                                self.rooms[slot[1][0]].rem_course(lecture2, slot[1][1])

                                room1.add_course(lecture2, slot[0][1])
                                self.rooms[slot[1][0]].add_course(lecture1, slot[1][1])


    def hillclimber_werk(self):
          """
          Moves students in werkgroep, based on a decreasing number of malus points.
          Nog niet toegepast op practica.
          """
          for nr, course in enumerate(self.courses): # Ga alle vakken langs
              groups_dict = {} # dict (key: group (1, 2, ...); value: set/list of students)
              nr_werk_groups = len(course.W)
              # print(f'len is {len(course.W)}')

              # Fill dict with groups and student lists
              for i in range(nr_werk_groups):
                  groups_dict[i+1] = course.W[i].studs

              # print(groups_dict)

              for nr1, werkcollege in enumerate(course.W):
                  group = int(werkcollege.type[1])
                  # groups_dict[group] = werkcollege.studs # set/list of student

                  for student in groups_dict[group]: # WELLICHT LOOP NAAR BUITEN VERPLAATSEN EN OVER STUDENTEN IN DICT HEEN LOOPEN
                      tries = {} # keys: ...; values: malus points

                      self.malus_count_old() # Tel minpunten
                      tries[group] = sum(self.malus)

                      # print(groups_dict[group])
                      # print(student)

                      groups_dict[group].remove(student) # In case of set: .discard(student)
                      werkcollege.studs = groups_dict[group] # Dit lecture object updaten

                      for i in range(nr_werk_groups):
                          other_group = i + 1
                          if other_group != group:
                              groups_dict[other_group].append(student)
                              course.W[i].studs = groups_dict[other_group] # Andere lecture object updaten

                              self.malus_count_old() # Tel minpunten
                              tries[other_group] = sum(self.malus)

                              groups_dict[i+1].remove(student)
                              course.W[i].studs = groups_dict[other_group] # Terug naar eerdere staat

                      # groups_dict[group].append(student)
                      groups_dict[group].append(student)
                      werkcollege.studs = groups_dict[group] # Terug naar originele staat


                      best_option = [k for k, v in tries.items() if v==min(tries.values())][0] # Select group in which the student can best be placed
                      # print(f'Best option to move student to is {best_option}')

                      if best_option != group: # Move student
                          groups_dict[group].remove(student)
                          werkcollege.studs = groups_dict[group] # Dit lecture object updaten (student verwijderen)

                          groups_dict[best_option].append(student)
                          course.W[best_option - 1].studs = groups_dict[best_option] # Andere lecture object updaten (student toevoegen)

                  self.malus_count_old()
                  print(self.malus, sum(self.malus), nr)

    def hillclimber_prac(self):
          """
          Moves students in werkgroep, based on a decreasing number of malus points.
          Nog niet toegepast op practica.
          """
          for nr, course in enumerate(self.courses): # Ga alle vakken langs
              groups_dict = {} # dict (key: group (1, 2, ...); value: set/list of students)
              nr_werk_groups = len(course.P)
              # print(f'len is {len(course.W)}')

              # Fill dict with groups and student lists
              for i in range(nr_werk_groups):
                  groups_dict[i+1] = course.P[i].studs

              # print(groups_dict)

              for nr1, werkcollege in enumerate(course.P):
                  group = int(werkcollege.type[1])
                  # groups_dict[group] = werkcollege.studs # set/list of student

                  for student in groups_dict[group]: # WELLICHT LOOP NAAR BUITEN VERPLAATSEN EN OVER STUDENTEN IN DICT HEEN LOOPEN
                      tries = {} # keys: ...; values: malus points

                      self.malus_count_old() # Tel minpunten
                      tries[group] = sum(self.malus)

                      # print(groups_dict[group])
                      # print(student)

                      groups_dict[group].remove(student) # In case of set: .discard(student)
                      werkcollege.studs = groups_dict[group] # Dit lecture object updaten

                      for i in range(nr_werk_groups):
                          other_group = i + 1
                          if other_group != group:
                              groups_dict[other_group].append(student)
                              course.P[i].studs = groups_dict[other_group] # Andere lecture object updaten

                              self.malus_count_old() # Tel minpunten
                              tries[other_group] = sum(self.malus)

                              groups_dict[i+1].remove(student)
                              course.P[i].studs = groups_dict[other_group] # Terug naar eerdere staat

                      # groups_dict[group].append(student)
                      groups_dict[group].append(student)
                      werkcollege.studs = groups_dict[group] # Terug naar originele staat


                      best_option = [k for k, v in tries.items() if v==min(tries.values())][0] # Select group in which the student can best be placed
                      # print(f'Best option to move student to is {best_option}')

                      if best_option != group: # Move student
                          groups_dict[group].remove(student)
                          werkcollege.studs = groups_dict[group] # Dit lecture object updaten (student verwijderen)

                          groups_dict[best_option].append(student)
                          course.P[best_option - 1].studs = groups_dict[best_option] # Andere lecture object updaten (student toevoegen)

                  self.malus_count_old()
                  print(self.malus, sum(self.malus), nr)


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
                        d['student'].append(stud.nr)
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

    def malus_count_old(self):
        '''
        Counts the amount of malus points from the output DataFrame
        '''
        # Different maluspoint counters
        double_hours = 0
        tussenuren = 0
        avondsloten = 0
        small_room = 0

        self.make_output()

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
            slots = sorted(list(count.keys()))
            # Check if the student more than 1 lecture this day
            tussen = slots[-1] - slots[0] - len(slots) + 1

            if tussen == 0:
                pass
            elif tussen == 1:
                tussenuren += 1
            elif tussen == 2:
                tussenuren += 3
            elif tussen == 3:
                # The rooster is not possible if a student has 3 tussenuren
                tussenuren += 10000

        # Check if any evening slots are used and give 5 point for each use
        for room in self.rooms:
            if room.evening:
                for avondslot in room.rooster[-1, :]:
                    if avondslot != 0:
                        avondsloten += 5

        # Check if rooms are overfull
        # Shouldn't be neccisarry if the rooster is made to only put lectures in rooms where they fit
        for room in self.rooms:
            for slot in np.ndindex(room.rooster.shape):
                if room.rooster[slot] != 0:
                    small_room += max(room.rooster[slot].size - room.capacity, 0)

        # Add up all the malus points for the total
        self.malus = double_hours, tussenuren, avondsloten, small_room

    def malus_count(self):
        self.malus = [0, 0, 0, 0]
        for student in self.student_list:
            self.malus[0] += student.malus[0]
            self.malus[1] += student.malus[1]
        for room in self.rooms:
            self.malus[2] += room.malus[0]
            self.malus[3] += room.malus[1]
