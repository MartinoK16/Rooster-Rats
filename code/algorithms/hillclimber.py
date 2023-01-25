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
        Does one loop over all the activities in a random order and finds the
        best fit for each of them by swapping with all other possibilities
        (activities or empty slots).
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

    def create_stud_set(self, stud_list, add_zero=True):
        stud_set = set(stud_list)
        if add_zero:
            stud_set.add(0)
        # print(stud_set)
        return stud_set

    def try_swap(self, student, group, new_group, new_group_nr, tries_dict, add_zero=True):
        for other_student in self.create_stud_set(new_group.studs, add_zero):
            self.swap_student(student, group, group.slot, other_student, new_group, new_group.slot)
            tries_dict[(new_group_nr, other_student)] = sum(Evaluation(self).malus_count())
            self.swap_student(other_student, group, group.slot, student, new_group, new_group.slot)
            return tries_dict

    def hc_students(self, tut_or_prac):
        """
        Accepts a string, 'T' for tutorial or 'P' for practical, and moves or
        swaps students to another tutorial group or practical group, based on a
        decreasing number of malus points.
        """
        # Loop over all courses randomly
        for nr, course in enumerate(random.sample(self.courses, len(self.courses))): # ENUMERATE WEGHALEN
            # Loop over all tutorial / practical groups
            for group_nr, group in enumerate(getattr(course, tut_or_prac)):
                # Loop over students in the group
                for student in group.studs:
                    # Dictionary to track the malus points for each student swap
                    tries = {}
                    malus = sum(Evaluation(self).malus_count())
                    tries[(group_nr, student)] = malus

                    # Consider each swapping option with other groups
                    for new_group_nr in range(len(getattr(course, tut_or_prac))):
                        new_group = getattr(course, tut_or_prac)[new_group_nr]

                        # Check if swapping and moving the student are possible
                        if new_group_nr != group_nr and new_group.max_studs > new_group.size:
                            self.try_swap(student, group, new_group, new_group_nr, tries)
                        elif new_group_nr != group_nr and new_group.max_studs == new_group.size:
                            self.try_swap(student, group, new_group, new_group_nr, tries, False)

                    # Randomly get one of the swaps with the least malus points
                    best_swap = random.choice([k for k, v in tries.items() if v==min(tries.values())])

                    # Select correct group and student
                    best_swap_group = getattr(course, tut_or_prac)[best_swap[0]]
                    best_swap_stud = best_swap[1]

                    # Perform this best swap if it is not equal to the current situation
                    self.swap_student(student, group, group.slot, best_swap_stud, best_swap_group, best_swap_group.slot)

                malus = Evaluation(self).malus_count()
                print((malus, nr, tut_or_prac), sum(malus))

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

    def swap_student(self, student1, lec1, slot1, student2, lec2, slot2):
        '''
        Removes a student from a lecture and adds it to another one.
        Also updates the student rooster and malus points
        '''
        if student1 != 0:
            lec1.studs.remove(student1)
            lec1.size -= 1
            lec2.studs.append(student1)
            lec2.size += 1
            student1.swap_lecture(lec1, slot1, lec2, slot2)

        if student2 != 0:
            lec2.studs.remove(student2)
            lec2.size -= 1
            lec1.studs.append(student2)
            lec1.size += 1
            student2.swap_lecture(lec2, slot2, lec1, slot1)

        lec1.room.update_malus()
        lec2.room.update_malus()
