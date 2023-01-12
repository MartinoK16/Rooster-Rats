class Room():
    def __init__(self, nr_timeslots, nr_days, room, evening, room_capacity, day, timeslot, course):
        self.nr_timeslots = nr_timeslots # Standard; without evening timeslot
        self.nr_days = nr_days
        self.room = room
        self.evening = evening # boolean
        self.capacity = room_capacity

        self.day = day
        self.timeslot = timeslot
        self.course = course

        # Create first version of rooster and availability
        if self.evening:
            self.availability = np.zeros((nr_timeslots + 1, nr_days))
            self.rooster = np.zeros((nr_timeslots + 1, nr_days))
        else:
            self.availability = np.zeros((nr_timeslots, nr_days))
            self.rooster = np.zeros((nr_timeslots, nr_days))

    def check_availability(self):
        """
        Accepts a 3D array of shape nr_rooms x nr_days x nr_timeslots and checks the
        availability for a given room. The function returns a boolean 3D array of
        shape nr_days x nr_timeslots which shows if the timeslot is occupied (True)
        or not (False).
        """
        # Check availability for the room; switch True and False (occupied = 1; not occupied = 0)
        self.availability = np.invert(self.rooster[self.room] == self.availability)

    def remove_course(self, timeslot):
        self.rooster[day, timeslot] = 0

    def add_course(self, timeslot):
        self.rooster[day, timeslot] = self.courses