import numpy as np

class Student():
    def __init__(self, stud_nr, nr_t, nr_d, courses):
        self.nr = stud_nr
        self.malus = [0, 0]
        self.courses = courses
        self.rooster = np.zeros((nr_t, nr_d), dtype=object)

    def add_lecture(self, lecture, slot):
        if self.rooster[slot] == 0:
            self.rooster[slot] = [lecture]
        else:
            self.rooster[slot].append(lecture)
        self.update_malus()

    def rem_lecture(self, lecture, slot):
        if self.rooster[slot] == 0: #or self.rooster[slot] == []:
            pass
        elif len(self.rooster[slot]) < 2:
            self.rooster[slot] = 0
        else:
            # for lec in self.rooster[slot]:
            #     print('Hallo', lec.code)
            # print('To Remove', lecture.code)
            # print()
            self.rooster[slot].remove(lecture)
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
