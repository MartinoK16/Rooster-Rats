import numpy as np

class Student():
    def __init__(self, stud_nr, nr_t, nr_d, courses):
        self.nr = stud_nr
        self.malus = [0, 0]
        self.courses = courses
        self.rooster = np.zeros((nr_t, nr_d), dtype=object)

    def swap_lecture(self, lec1, lec2, slot):
        if lec1 != 0:
            if len(self.rooster[slot]) == 1:
                self.rooster[slot] = 0
            else:
                self.rooster[slot].remove(lec1)

        if lec2 != 0:
            if self.rooster[slot] == 0:
                self.rooster[slot] = [lec2]
            else:
                self.rooster[slot].append(lec2)

        self.update_malus()

    def update_malus(self):
        self.malus = [0, 0]
        for slot in list(zip(*np.nonzero(self.rooster!=0))):
            self.malus[0] += len(self.rooster[slot]) - 1

        for col in self.rooster.T:
            slots = np.nonzero(col)[0]
            if len(slots) > 0:
                tus = slots[-1] - slots[0] - len(slots) + 1
                if tus == 1:
                    self.malus[1] += 1
                elif tus == 2:
                    self.malus[1] += 3
                # The rooster is not possible if a student has 3 tussenuren
                elif tus == 3:
                    self.malus[1] += 10000
