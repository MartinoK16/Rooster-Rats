import random
import copy
import time
from .evaluation import *
from .hillclimber import *

class Tabu():
    def __init__(self, rooster):
        self.rooms = rooster.rooms
        self.courses = rooster.courses
        self.students = rooster.students
        self.activities = rooster.activities

    def tabu_search(self, max_size):
        '''
        Kies een initiële oplossing en bepaal hoe goed die oplossing is
        Herhaal
            Bepaal de naburige oplossingen die niet taboe zijn en bepaal hoe goed deze zijn
            Kies de beste naburige oplossing en plaats de vorige oplossing in de Tabu lijst
            Als de nieuwe oplossing beter is onthoud dan de nieuwe oplossing
        Tot de stop-conditie vervuld is
        '''
        best = [tuple(sorted(Evaluation(self).rooster_dict().items())), sum(Evaluation(self).malus_count())]
        tabu_list = [best[0]]
        nr = 0

        while True:
            # self.hc_students('T')
            # self.hc_students('P')
            neighbours = self.get_neighbours()
            nr += 1
        # for nr, act in enumerate(self.activities):
        #     neighbours = self.get_neighbours(act)
            best_cand = list(neighbours.items())[0]
            for cand in list(neighbours.items()):
                if cand[0] not in tabu_list and cand[1] < best_cand[1]:
                    best_cand = cand

            if best_cand[1] < best[1]:
                print('BETTER')
                best = copy.deepcopy(best_cand)

            self.rooster_object(dict(best_cand[0]))
            tabu_list.append(best_cand[0])
            if len(tabu_list) > max_size:
                tabu_list.pop(0)

            malus = Evaluation(self).malus_count()
            print(malus, sum(malus), len(tabu_list), nr)

        return best

    def get_neighbours(self):
        st = time.time()
        tries = {}
        for nr3, act1 in enumerate(random.sample(self.activities, len(self.activities))):
            tries2 = [(tuple(sorted(Evaluation(self).rooster_dict().items())), act1, 0)]
            prev_malus = sum(Evaluation(self).malus_count())
            room1 = act1.room
            slot1 = act1.slot
            # start = Evaluation(self).rooster_dict()
            # Loop over all the slots in each room
            for nr2, room2 in enumerate(self.rooms):
                for slot2 in np.ndindex(room2.rooster.shape):
                    # Get which lecture is placed in this room and slot
                    act2 = room2.rooster[slot2]
                    # Swap these 2 activities, get the new malus and put it in the dict and swap them back
                    self.swap_course(room1, act1, slot1, room2, act2, slot2)

                    # for act in [act1, act2]:
                    #     if act != 0:
                    #         if act.type[0] != 'L':
                    #             for course in self.courses:
                    #                 if act.name == course.name:
                    #                     self.hc_students([course], act.type[0])

                    if sum(Evaluation(self).malus_count()) < prev_malus:
                        tries2 = [(tuple(sorted(Evaluation(self).rooster_dict().items())), act1, act2)]
                        prev_malus = sum(Evaluation(self).malus_count())

                    elif sum(Evaluation(self).malus_count()) == prev_malus:
                        tries2.append((tuple(sorted(Evaluation(self).rooster_dict().items())), act1, act2))

                    # self.rooster_object(start)
                    self.swap_course(room1, act2, slot1, room2, act1, slot2)

            chosen_try = random.choice(tries2)
            # print(chosen_try)
            # print(chosen_try[0])
            self.rooster_object(dict(chosen_try[0]))

            for act in chosen_try[1:]:
                if act != 0:
                    if act.type[0] != 'L':
                        for course in self.courses:
                            if act.name == course.name:
                                self.group_swap(course, act.type[0])

            tries[tuple(sorted(Evaluation(self).rooster_dict().items()))] = sum(Evaluation(self).malus_count())

            print(nr3, 'Execution time malus:', time.time() - st, 'seconds')
        return tries

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
                stud.swap_activity(lec1, slot1, lec1, slot2)

        # Check if it is a lecture and not an empty slot
        if lec2 != 0:
            # Update the lecture attributes
            lec2.room = room1
            lec2.slot = slot1
            # Update all the roosters for the students with this lecture
            for stud in lec2.studs:
                stud.swap_activity(lec2, slot2, lec2, slot1)

        # Update the malus counts for both rooms
        room1.update_malus()
        room2.update_malus()


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

                    for i in range(nr_werk_groups):
                        new_group_nr = i + 1
                        new_group = getattr(course, tut_or_prac)[i]

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

            # malus = Evaluation(self).malus_count()
            # print(malus, nr, tut_or_prac, sum(malus))

    def group_swap(self, course, tut_or_prac): # OLD VERSION
        """
        Accepts a string, 'T' for tutorial or 'P' for practical, and moves or
        swaps students to another tutorial group or practical group, based on a
        decreasing number of malus points.
        """
        nr_werk_groups = len(getattr(course, tut_or_prac))

        for group in getattr(course, tut_or_prac):
            group_nr = int(group.type[1])

            for student in group.studs:
                tries = {} # key = group nr, value = malus
                tries2 = {} # key = list of group nr and student index; value = malus
                malus = sum(Evaluation(self).malus_count())
                tries[group_nr] = malus
                tries2[student] = malus

                for i in range(nr_werk_groups):
                    new_group_nr = i + 1
                    new_group = getattr(course, tut_or_prac)[i]

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

        # malus = Evaluation(self).malus_count()
        # print(malus, nr, tut_or_prac, sum(malus))

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

        # Remove lec1 and add lec2 to student rooster
        student1.swap_activity(act1, slot1, act2, slot2)
        student2.swap_activity(act2, slot2, act1, slot1)

    def rooster_object(self, rooster_dict):
        for stud in self.students:
            stud.clear_rooster()

        for slot in list(rooster_dict.items()):
            for room in self.rooms:
                if room.name == slot[0][0]:
                    break

            if slot[1] != 0:
                for act in self.activities:
                    if act.code == slot[1][0]:
                        break

                studs = []
                for stud in self.students:
                    if stud.nr in slot[1][1]:
                        studs.append(stud)

                act.studs = studs
                room.swap_course(0, act, slot[0][1])
            else:
                room.rooster[slot[0][1]] = 0
                room.update_malus()
