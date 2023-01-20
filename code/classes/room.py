import numpy as np

class Room():
    def __init__(self, nr_timeslots, nr_days, room, evening, room_capacity):
        # Initialize all the required variables
        self.room = room
        self.evening = evening # Bool
        self.capacity = room_capacity
        self.malus = [0, 0]

        # Create empty version of rooster with possible eveningslots
        if self.evening:
            self.rooster = np.zeros((nr_timeslots + 1, nr_days), dtype=object)
        else:
            self.rooster = np.zeros((nr_timeslots, nr_days), dtype=object)

    def swap_course(self, lec1, lec2, slot):
        '''
        Removes and adds a lecture from a slot and updates it room and slot attribute.
        '''
        # Set the room rooster to the new lecture
        self.rooster[slot] = lec2

        # Remove the old lecture
        if lec1 != 0:
            # Update room and slot of the lecture
            lec1.room = None
            lec1.slot = None
            # Update the rooster of the students in the lecture
            for stud in lec1.studs:
                stud.swap_lecture(lec1, slot, 0, slot)

        # Add the new lecture
        if lec2 != 0:
            # Update room and slot of the lecture
            lec2.room = self
            lec2.slot = slot
            # Update the rooster of the students in the lecture
            for stud in lec2.studs:
                stud.swap_lecture(0, slot, lec2, slot)

        # Recalculate the malus points for this room
        self.update_malus()

    def update_malus(self):
        '''
        Updates the malus points for this room
        '''
        # Start counting from 0
        self.malus = [0, 0]

        # Check if any of the slots have to large groups
        for slot in list(zip(*np.nonzero(self.rooster))):
            if self.rooster[slot].size > self.capacity:
                self.malus[1] += self.rooster[slot].size - self.capacity

        # If the rooms has evenings slots check how many are used
        if self.evening:
            for slot in list(zip(*np.nonzero(self.rooster[-1,:]))):
                self.malus[0] += 5
