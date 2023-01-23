import numpy as np

class Student():
    def __init__(self, stud_nr, nr_t, nr_d, courses):
        # Initialize all the required variables
        self.nr = stud_nr
        self.malus = [0, 0]
        self.courses = courses
        self.rooster = np.zeros((nr_t, nr_d), dtype=object)

    def swap_lecture(self, lec1, slot1, lec2, slot2):
        '''
        Swaps lec1 from slot1 to lec2 in slot2 in the rooster
        '''
        # Remove the old lecture from the rooster
        if lec1 != 0:
            if len(self.rooster[slot1]) == 1:
                self.rooster[slot1] = 0
            else:
                self.rooster[slot1].remove(lec1)

        # Add the new lecture to the rooster
        if lec2 != 0:
            if self.rooster[slot2] == 0:
                self.rooster[slot2] = [lec2]
            else:
                self.rooster[slot2].append(lec2)

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
<<<<<<< HEAD
                    self.malus[1] += 10000
=======
                    self.malus[1] += 10
>>>>>>> 997f0d3 (simulated annealing)
