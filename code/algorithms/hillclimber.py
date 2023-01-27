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
        for nr3, activity1 in enumerate(random.sample(self.activities, len(self.activities))):
            # Get the room and slot where this activity is place now
            room1 = activity1.room
            slot1 = activity1.slot
            # Make a dictionary to track the malus points for each slot
            tries = {}
            # Loop over all the slots in each room
            for nr2, room2 in enumerate(self.rooms):
                for slot2 in np.ndindex(room2.rooster.shape):
                    # Get which activity is placed in this room and slot
                    activity2 = room2.rooster[slot2]
                    # Swap these 2 activities, get the new malus and put it in the dict and swap them back
                    self.swap_course(room1, activity1, slot1, room2, activity2, slot2)
                    tries[nr2, slot2] = sum(Evaluation(self).malus_count())
                    self.swap_course(room1, activity2, slot1, room2, activity1, slot2)

            # Randomly get one of the slots with the least malus points
            slot = random.choice([k for k, v in tries.items() if v==min(tries.values())])

            # Get which room and activity need to be switched and swap them
            room2 = self.rooms[slot[0]]
            activity2 = room2.rooster[slot[1]]
            self.swap_course(room1, activity1, slot1, room2, activity2, slot[1])

            # Get the updated malus count and print useful info
            malus = Evaluation(self).malus_count()
            print(activity1.code, malus, sum(malus), nr3)


    def hc_students(self, tut_or_prac): # OLD VERSION
        """
        Accepts a string, 'T' for tutorial or 'P' for practical, and moves or
        swaps students to another tutorial group or practical group, based on a
        decreasing number of malus points.
        """
        for nr, course in enumerate(random.sample(self.courses, len(self.courses))): # Ga alle vakken langs         # ENUMERATE WEGHALEN
            nr_werk_groups = len(getattr(course, tut_or_prac))

            for group in getattr(course, tut_or_prac):
                group_nr = int(group.type[1])

                for student in group.studs:
                    tries = {} # key = group nr, value = malus
                    tries2 = {} # key = list of group nr and student index; value = malus
                    malus = sum(Evaluation(self).malus_count())
                    tries[group_nr] = malus
                    tries2[student] = malus

                    # Consider each swapping option with other groups
                    for new_group_nr, new_group in enumerate(getattr(course, tut_or_prac)):
                        # Check if capacity is not already reached before swapping or moving the student
                        if new_group_nr != group_nr and new_group.max_studs > new_group.size:
                            self.try_swap(student, group, new_group, new_group_nr, tries)
                        elif new_group_nr != group_nr and new_group.max_studs == new_group.size:
                            self.try_swap(student, group, new_group, new_group_nr, tries, False)

                        if new_group_nr != group_nr:
                            for nr1, other_student in enumerate(new_group.studs):
                                self.swap_student(student, group, group.slot, other_student, new_group, new_group.slot)
                                tries2[(new_group_nr, other_student)] = sum(Evaluation(self).malus_count())
                                self.swap_student(other_student, group, group.slot, student, new_group, new_group.slot)

                    best_move_nr = random.choice([k for k, v in tries.items() if v==min(tries.values())]) # Select group in which the student can best be placed
                    move_malus = tries[best_move_nr]
                    best_move = getattr(course, tut_or_prac)[best_move_nr - 1]

                    best_swap_try = random.choice([k for k, v in tries2.items() if v==min(tries2.values())]) # Select group in which the student can best be placed

                    # Als de originele maluscount (met key = studentnummer) niet de laagste is bij swappen
                    if best_swap_try != student:
                        best_swap_nr = best_swap_try[0] # Correct group to swap the student to
                        best_swap_stud = best_swap_try[1] # Index to search the right student
                        swap_malus = tries2[best_swap_try]
                        best_swap = getattr(course, tut_or_prac)[best_swap_nr - 1]

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

            malus = Evaluation(self).malus_count()
            print(malus, nr, tut_or_prac, sum(malus))

    def swap_course(self, room1, act1, slot1, room2, act2, slot2):
        '''
        Accepts two rooms, their activities and slots. Swaps two activities from
        room and slot and updates the corresponding student roosters.
        '''
        # Swap the 2 activities in the room roosters
        room1.rooster[slot1] = act2
        room2.rooster[slot2] = act1

        # Check if it is an activity and not an empty slot
        if act1 != 0:
            # Update the activity attributes
            act1.room = room2
            act1.slot = slot2
            # Update all the roosters for the students with this activity
            for stud in act1.studs:
                stud.swap_activity(act1, slot1, act1, slot2)

        # Check if it is an activity and not an empty slot
        if act2 != 0:
            # Update the activity attributes
            act2.room = room1
            act2.slot = slot1
            # Update all the roosters for the students with this activity
            for stud in act2.studs:
                stud.swap_activity(act2, slot2, act2, slot1)

        # Update the malus counts for both rooms
        room1.update_malus()
        room2.update_malus()


    def move_student(self, student, act1, slot1, act2, slot2): # OLD VERSION
        '''
        Removes a student from a lecture and adds it to another one.
        Also updates the student rooster and malus points
        '''
        act1.studs.remove(student)
        act1.size -= 1
        act1.room.update_malus()
        act2.studs.append(student)
        act2.size += 1
        act2.room.update_malus()
        # Remove lec1 and add lec2 to student rooster
        student.swap_activity(act1, slot1, act2, slot2)

    def swap_student(self, student1, act1, slot1, student2, act2, slot2): # OLD VERSION
        '''
        Removes a student from a lecture and adds it to another one.
        Also updates the student rooster and malus points
        '''
        act1.studs.remove(student1)
        act2.studs.append(student1)
        act2.studs.remove(student2)
        act1.studs.append(student2)

    def create_stud_set(self, stud_list, add_zero=True):
        '''
        Accepts a list and an optional boolean argument. Transforms list into
        set, either with or without adding 0 (True vs. False, respectively).
        '''
        stud_set = set(stud_list)
        if add_zero:
            stud_set.add(0)
        return stud_set


    def try_swap(self, student, group, new_group, new_group_nr, tries, add_zero=True):
        '''
        Accepts student to be swapped, current group of the student, new group,
        number of the new group, a tries dictionary and an optional boolean
        argument. Transforms student list of new group into set, swaps students,
        gets the new malus, puts it in the dictionary and swaps them back.
        '''
        for other_student in self.create_stud_set(new_group.studs, add_zero):
            self.swap_student(student, group, group.slot, other_student, new_group, new_group.slot)
            tries[(new_group_nr, other_student)] = sum(Evaluation(self).malus_count())
            self.swap_student(other_student, group, group.slot, student, new_group, new_group.slot)
        return tries
