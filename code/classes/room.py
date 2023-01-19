import numpy as np

class Room():
    def __init__(self, nr_timeslots, nr_days, room, evening, room_capacity):
        self.room = room # object or integer
        self.evening = evening # boolean
        self.capacity = room_capacity

        # Create empty version of rooster
        if self.evening:
            self.rooster = np.zeros((nr_timeslots + 1, nr_days), dtype=object)
        else:
            self.rooster = np.zeros((nr_timeslots, nr_days), dtype=object)

    def remove_course(self, slot):
        self.rooster[slot] = 0

    def add_course(self, lecture, slot):
        self.rooster[slot] = lecture
