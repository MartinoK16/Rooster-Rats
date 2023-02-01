import copy
import random
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
        Take an initial rooster and get the malus count for it
        Loop for #iterations
            Get the neighbours for this state and the corresponding malus points
            If there is a better rooster, remember this rooster
            Put the last state in the tabu list
        Return the best seen rooster
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
            # Randomly get a candidate from the neighbours to start
            best_cand = random.choice(neighbours)
            # Loop over all the neighbours
            for cand in random.sample(neighbours, len(neighbours)):
                # Check if this rooster is not in the tabu list and malus is lower
                if cand[0] not in tabu_list and cand[1] < best_cand[1]:
                    # Set the best candidate to this candidate
                    best_cand = cand

            # If this best candidate is better than the best found rooster set it to the best
            if best_cand[1] < self.best[1]:
                print('BETTER')
                self.best = copy.deepcopy(best_cand)
                self.iter = (nr, self.best[1])

            # Update self to use the rooster of the best candidate
            self.students, self.rooms, self.activities = \
            Evaluation(self).rooster_object(dict(best_cand[0]))

            # Append the best candidate to the tabu list
            tabu_list.append(best_cand[0])
            # Remove the first entry of the list
            if len(tabu_list) > max_size:
                tabu_list.pop(0)

            malus = Evaluation(self).malus_count()
            print(malus, sum(malus), self.best[1], nr)
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
                Hillclimber(self).swap_course(room1, act1, slot1, room2, act2, slot2)
                tries[Evaluation(self).rooster_dict()] = sum(Evaluation(self).malus_count())
                Hillclimber(self).swap_course(room1, act2, slot1, room2, act1, slot2)

        return list(tries.items())
