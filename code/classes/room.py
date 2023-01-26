import numpy as np

class Room():
    def __init__(self, timeslots, days, room, evening, capacity):
        # Initialize all the required variables
        self.name = room
        self.evening = evening # Bool
        self.capacity = capacity
        self.malus = [0, 0]

        # Create empty version of rooster with possible eveningslots
        if self.evening:
            self.rooster = np.zeros((timeslots + 1, days), dtype=object)
        else:
            self.rooster = np.zeros((timeslots, days), dtype=object)

    def swap_course(self, act1, act2, slot):
        '''
        Removes and adds a lecture from a slot and updates it room and slot attribute.
        '''
        # Set the room rooster to the new lecture
        self.rooster[slot] = act2

        # Remove the old lecture
        if act1 != 0:
            # Update room and slot of the lecture
            act1.room = None
            act1.slot = None
            # Update the rooster of the students in the lecture
            for stud in act1.studs:
                stud.swap_activity(act1, slot, 0, slot)

        # Add the new lecture
        if act2 != 0:
            # Update room and slot of the lecture
            act2.room = self
            act2.slot = slot
            # Update the rooster of the students in the lecture
            for stud in act2.studs:
                stud.swap_activity(0, slot, act2, slot)

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
