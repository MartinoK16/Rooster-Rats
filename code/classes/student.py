import numpy as np

class Student():
    def __init__(self, nr, timeslots, days, courses):
        # Initialize all the required variables
        self.nr = nr
        self.malus = [0, 0]
        self.courses = courses
        self.rooster = np.zeros((timeslots, days), dtype=object)

    def clear_rooster(self):
        self.rooster = np.zeros(self.rooster.shape, dtype=object)

    def swap_activity(self, act1, slot1, act2, slot2):
        '''
        Swaps act1 from slot1 to act2 in slot2 in the rooster
        '''
        # Remove the old lecture from the rooster
        if act1 != 0:
            if self.rooster[slot1] == [act1]:
                self.rooster[slot1] = 0
            else:
                # print(act1.code, self.rooster)
                self.rooster[slot1].remove(act1)

        # Add the new lecture to the rooster
        if act2 != 0:
            if self.rooster[slot2] == 0:
                self.rooster[slot2] = [act2]
            else:
                self.rooster[slot2].append(act2)

        # Recalculate the malus points for this student
        self.update_malus()

    def update_malus(self):
        '''
        Updates the malus points for this student
        '''
        # Start counting from 0
        self.malus = [0, 0]
        # Check how many double lectures are in the rooster
        for slot in list(zip(*np.nonzero(self.rooster))):
            self.malus[0] += len(self.rooster[slot]) - 1

        # Check if the rooster has tussenuren
        for day in self.rooster.T:
            slots = np.nonzero(day)[0]
            if len(slots) > 0:
                tus = slots[-1] - slots[0] - len(slots) + 1
                if tus == 1:
                    self.malus[1] += 1
                elif tus == 2:
                    self.malus[1] += 3
                # The rooster is not possible if a student has 3 tussenuren
                elif tus == 3:
                    self.malus[1] += 10000
