import numpy as np
import random
from .evaluation import *

class Hillclimber():
    def __init__(self, rooster):
        self.rooms = rooster.rooms
        self.courses = rooster.courses
        self.students = rooster.students
        self.activities = rooster.activities

    def hc_activities(self):
        '''
        Does one loop over all the activities and finds the best fit for each of them
        by swapping with all other possibilities (activities or empty slots)
        '''
        # Loop over all the activities randomly
        for nr3, lecture1 in enumerate(random.sample(self.activities, len(self.activities))):
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
                    # Swap these 2 activities, get the new malus and put it in the dict and swap them back
                    self.swap_course(room1, lecture1, slot1, room2, lecture2, slot2)
                    tries[nr2, slot2] = sum(Evaluation(self).malus_count())
                    self.swap_course(room1, lecture2, slot1, room2, lecture1, slot2)

            # Randomly get one of the slots with the least malus points
            slot = random.choice([k for k, v in tries.items() if v==min(tries.values())])

            # Get which room and lecture need to be switched and swap them
            room2 = self.rooms[slot[0]]
            lecture2 = room2.rooster[slot[1]]
            self.swap_course(room1, lecture1, slot1, room2, lecture2, slot[1])

            # Get the updated malus count and print useful info
            malus = Evaluation(self).malus_count()
            print(lecture1.code, malus, sum(malus), nr3)

    def hc_students(self, werk_or_prac):
        """
        Moves students in werkgroep or practicumgroep, based on a decreasing
        number of malus points.
        """
        for nr, course in enumerate(random.sample(self.courses, len(self.courses))): # Ga alle vakken langs
            nr_werk_groups = len(getattr(course, werk_or_prac))

            for group in getattr(course, werk_or_prac):
                group_nr = int(group.type[1])

                for student in group.studs:
                    tries = {} # key = group nr, value = malus
                    tries2 = {} # key = list of group nr and student index; value = malus
                    malus = sum(Evaluation(self).malus_count())
                    tries[group_nr] = malus
                    tries2[student] = malus

                    for i in range(nr_werk_groups):
                        new_group_nr = i + 1
                        new_group = getattr(course, werk_or_prac)[i]

                        if new_group_nr != group_nr and new_group.max_studs > new_group.size: # Houd rekening met maximale aantal studenten per werkgroep
                            self.move_student(student, group, group.slot, new_group, new_group.slot)
                            tries[new_group_nr] = sum(Evaluation(self).malus_count()) # Maluspunten voor eventuele nieuwe groep
                            self.move_student(student, new_group, new_group.slot, group, group.slot)

                        if new_group_nr != group_nr:
                            for nr1, other_student in enumerate(new_group.studs):
                                self.swap_student(student, group, group.slot, other_student, new_group, new_group.slot)
                                tries2[(new_group_nr, other_student)] = sum(Evaluation(self).malus_count())
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

            # malus = Evaluation(self).malus_count()
            # print(malus, malus, nr, werk_or_prac)

    def swap_course(self, room1, lec1, slot1, room2, lec2, slot2):
        '''
        Swaps 2 activities from room and slot and updates the corresponding student roosters
        '''
        # Swap the 2 activities in the room roosters
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
