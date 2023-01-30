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

    def tabu_search(self, max_size, max_iter):
        '''
        Kies een initiële oplossing en bepaal hoe goed die oplossing is
        Herhaal
            Bepaal de naburige oplossingen die niet taboe zijn en bepaal hoe goed deze zijn
            Kies de beste naburige oplossing en plaats de vorige oplossing in de Tabu lijst
            Als de nieuwe oplossing beter is onthoud dan de nieuwe oplossing
        Tot de stop-conditie vervuld is
        '''
        self.maluses = []
        # Set the input rooster as the best rooster that was seen and get the malus points
        self.best = [Evaluation(self).rooster_dict(), sum(Evaluation(self).malus_count())]
        # Add the input rooster to the tabu list
        tabu_list = [self.best[0]]

        # Loop for max_iter iterations
        for nr in range(max_iter):
            # Get the neighbours for this rooster
            neighbours = self.get_neighbours()
            # Randomly get 
            best_cand = random.choice(neighbours)
            for cand in random.sample(neighbours, len(neighbours)):
                if cand[0] not in tabu_list and cand[1] < best_cand[1]:
                    best_cand = cand

            if best_cand[1] < self.best[1]:
                print('BETTER')
                self.best = copy.deepcopy(best_cand)
                self.iter = (nr, self.best[1])

            self.students, self.rooms, self.activities, self.activities = \
            Evaluation(self).rooster_object(dict(best_cand[0]))

            tabu_list.append(best_cand[0])
            if len(tabu_list) > max_size:
                tabu_list.pop(0)

            malus = Evaluation(self).malus_count()
            print(malus, sum(malus), len(tabu_list), nr)
            self.maluses.append(sum(malus))

    def get_neighbours(self):
        '''
        Returns a list of all the neighbours and malus counts from the original
        state by switching an activity
        '''
        act1 = random.choice(self.activities)
        tries = {}
        room1 = act1.room
        slot1 = act1.slot
        # Loop over all the slots in each room
        for nr2, room2 in enumerate(self.rooms):
            for slot2 in np.ndindex(room2.rooster.shape):
                # Get which lecture is placed in this room and slot
                act2 = room2.rooster[slot2]
                # Swap these 2 activities, get the new malus and put it in the dict and swap them back
                self.swap_course(room1, act1, slot1, room2, act2, slot2)
                tries[Evaluation(self).rooster_dict()] = sum(Evaluation(self).malus_count())
                self.swap_course(room1, act2, slot1, room2, act1, slot2)

        return list(tries.items())

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

    def rooster_object(self, rooster_dict):
        '''
        Updates all the students, rooms and activities to get the rooster from
        the given dictionary
        '''
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
