import numpy as np
import random
from .evaluation import *

class Initialize():
    def __init__(self, rooster):
        self.rooms = rooster.rooms
        self.courses = rooster.courses
        self.student_list = rooster.student_list
        self.lectures_list = rooster.lectures_list

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

    def make_rooster_largetosmall(self):
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

    def make_rooster_greedy(self):
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
                    tries[nr, (slot)] = sum(Evaluation(self).malus_count())
                    room.swap_course(lecture, 0, slot)

            # Randomly get one of the slots with the least malus points
            slot = random.choice([k for k, v in tries.items() if v==min(tries.values())])
            # Add the lecture to this room and slot
            self.rooms[slot[0]].swap_course(0, lecture, slot[1])

            # Get the updated malus count and print useful info
            malus = Evaluation(self).malus_count()
            print(lecture.code, malus, sum(malus), lecture.size)
