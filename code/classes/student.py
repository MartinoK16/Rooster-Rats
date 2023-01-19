import numpy as np

class Student():
    def __init__(self, stud_nr, nr_timeslots, nr_days):
        self.nr = stud_nr
        self.rooster = np.zeros((nr_timeslots, nr_days), dtype=object)
        self.rooster[0,:] = [1]
        self.rooster[3,:] = [1]
        self.rooster[2, 2] = [1, 2]

    def update_malus(self):
        self.malus = [0, 0]
        for col in self.rooster.T:
            slots = np.nonzero(col)[0]
            tus = slots[-1] - slots[0] - len(slots) + 1
            if tus == 1:
                self.malus[1] += 1
            elif tus == 2:
                self.malus[1] += 3
            # The rooster is not possible if a student has 3 tussenuren
            elif tus == 3:
                self.malus[1] += 10000


        print(self.malus)

stud = Student(111, 5, 5)
stud.update_malus()
