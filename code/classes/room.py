import numpy as np

class Room():
    def __init__(self, nr_timeslots, nr_days, room, evening, room_capacity):
        self.room = room # room name
        self.evening = evening # boolean
        self.capacity = room_capacity
        self.malus = [0, 0]

        # Create empty version of rooster
        if self.evening:
            self.rooster = np.zeros((nr_timeslots + 1, nr_days), dtype=object)
        else:
            self.rooster = np.zeros((nr_timeslots, nr_days), dtype=object)

    def swap_course(self, lec1, lec2, slot):
        self.rooster[slot] = lec2

        # Remove the old lecture
        if lec1 != 0:
            lec1.room = None
            lec1.slot = None
            for stud in lec1.studs:
                stud.swap_lecture(lec1, 0, slot)

        # Add the new lecture
        if lec2 != 0:
            lec2.room = self
            lec2.slot = slot
            for stud in lec2.studs:
                stud.swap_lecture(0, lec2, slot)

        self.update_malus()

    def update_malus(self):
        self.malus = [0, 0]

        for slot in list(zip(*np.nonzero(self.rooster))):
            if self.rooster[slot].size > self.capacity:
                self.malus[1] += self.rooster[slot].size - self.capacity

        if self.evening:
            for slot in list(zip(*np.nonzero(self.rooster[-1,:]))):
                self.malus[0] += 5
