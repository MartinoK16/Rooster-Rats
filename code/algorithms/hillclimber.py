import numpy as np
import random
from .evaluation import *

class Hillclimber():
    def __init__(self, rooster):
        self.rooms = rooster.rooms
        self.courses = rooster.courses
        self.students = rooster.students
        self.activities = rooster.activities
        # List to store malus count for each iteration
        self.maluses = []

    def hc_activities(self):
        '''
        Loops over all the activities once in a random order and finds the
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
            self.maluses.append(sum(malus))

    def hc_students(self, tut_or_prac):
        '''
        Accepts a string, 'T' for tutorial or 'P' for practical, and loops over
        all the courses in a random order. Finds the best fit for each student
        in tutorial or practical groups by swapping with all other possibilities
        (students or empty spots).
        '''
        # Loop over all courses randomly
        for nr, course in enumerate(random.sample(self.courses, len(self.courses))): # ENUMERATE WEGHALEN
            # Loop over all students in each tutorial / practical group
            for group_nr, group in enumerate(getattr(course, tut_or_prac)):
                for student in group.studs:
                    # Dictionary to track the malus points for each student swap
                    tries = {}
                    malus = sum(Evaluation(self).malus_count())
                    tries[(group_nr, student)] = malus

                    # Consider each swapping option with other groups
                    for new_group_nr, new_group in enumerate(getattr(course, tut_or_prac)):
                        # Check if capacity is not already reached before swapping or moving the student
                        if new_group_nr != group_nr and new_group.max_studs > new_group.size:
                            self.try_swap(student, group, new_group, new_group_nr, tries)
                        elif new_group_nr != group_nr and new_group.max_studs == new_group.size:
                            self.try_swap(student, group, new_group, new_group_nr, tries, False)

                    # Randomly get one of the swaps with the least malus points
                    best_swap = random.choice([k for k, v in tries.items() if v==min(tries.values())])

                    # Select correct group and student and perform best swap
                    best_swap_group = getattr(course, tut_or_prac)[best_swap[0]]
                    best_swap_stud = best_swap[1]
                    self.swap_student(student, group, group.slot, best_swap_stud, best_swap_group, best_swap_group.slot)

                # Get the updated malus count and print useful info
                malus = Evaluation(self).malus_count()
                print((malus, nr, tut_or_prac), sum(malus))

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

    def swap_student(self, student1, act1, slot1, student2, act2, slot2):
        '''
        Accepts two students with two activities and two timeslots. Removes 
        both students from their lecture and adds them to the other one.
        Also updates the student rooster and malus points.
        '''
        # Move student 1 and update the occupation of the activity group
        if student1 != 0:
            act1.studs.remove(student1)
            act1.size -= 1
            act2.studs.append(student1)
            act2.size += 1
            student1.swap_activity(act1, slot1, act2, slot2)
        
        # Move student 2 and update the occupation of the activity group
        if student2 != 0:
            act2.studs.remove(student2)
            act2.size -= 1
            act1.studs.append(student2)
            act1.size += 1
            student2.swap_activity(act2, slot2, act1, slot1)
        
        # Update the malus counts for both rooms
        act1.room.update_malus()
        act2.room.update_malus()

    def create_stud_set(self, stud_list, add_zero=True):
        '''
        Accepts a list and an optional boolean argument. Transforms list into
        set, either with or without adding 0 (True vs. False, respectively).
        '''
        # Transform list into set, either with or without adding zero
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
            # Swap two students with each other or move student to another lecture
            self.swap_student(student, group, group.slot, other_student, new_group, new_group.slot)
            # Store malus count resulting from this swap
            tries[(new_group_nr, other_student)] = sum(Evaluation(self).malus_count())
            # Swap students or move student back to their original lecture
            self.swap_student(other_student, group, group.slot, student, new_group, new_group.slot)
        return tries
