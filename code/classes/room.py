import numpy as np

class Room():
    def __init__(self, nr_timeslots, nr_days, room, evening, room_capacity):
        self.room = room # object or integer
        self.evening = evening # boolean
        self.capacity = room_capacity
        self.malus = [0, 0]

        # Create empty version of rooster
        if self.evening:
            self.rooster = np.zeros((nr_timeslots + 1, nr_days), dtype=object)
        else:
            self.rooster = np.zeros((nr_timeslots, nr_days), dtype=object)

    def remove_course(self, lecture, slot):
        self.rooster[slot] = 0
        for stud in lecture.studs:
            stud.rem_lecture(lecture, slot)
        self.update_malus()

    def add_course(self, lecture, slot):
        self.rooster[slot] = lecture
        for stud in lecture.studs:
            stud.add_lecture(lecture, slot)
        self.update_malus()

    def update_malus(self):
        self.malus = [0, 0]
        for slot in list(zip(*np.nonzero(self.rooster))):
            if self.rooster[slot].size > self.capacity:
                self.malus[1] += self.rooster[slot].size - self.capacity
        if self.evening:
            for slot in list(zip(*np.nonzero(self.rooster[-1,:]))):
                self.malus[0] += 5
