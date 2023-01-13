import numpy as np

class Room():
    def __init__(self, nr_timeslots, nr_days, room, evening, room_capacity):
        self.nr_timeslots = nr_timeslots # Standard; without evening timeslot
        self.nr_days = nr_days
        self.room = room # object or integer
        self.evening = evening # boolean
        self.capacity = room_capacity

        # Create first version of rooster and availability
        if self.evening:
            self.availability = np.ones((nr_timeslots + 1, nr_days), dtype=bool)
            self.rooster = np.zeros((nr_timeslots + 1, nr_days), dtype=object)
        else:
            self.availability = np.ones((nr_timeslots, nr_days), dtype=bool)
            self.rooster = np.zeros((nr_timeslots, nr_days), dtype=object)

    def check_availability(self):
        """
        Accepts a 3D array of shape nr_rooms x nr_days x nr_timeslots and checks the
        availability for a given room. The function returns a boolean 3D array of
        shape nr_days x nr_timeslots which shows if the timeslot is occupied (False)
        or not (True).
        """
        # Check availability for the room; switch True and False (occupied = 1; not occupied = 0)
        self.availability = np.invert(self.rooster == self.availability)

    def remove_course(self, slot):
        self.rooster[slot] = 0
        self.availability[slot] = True

    def add_course(self, course, slot):
        self.rooster[slot] = course
        self.availability[slot] = False
