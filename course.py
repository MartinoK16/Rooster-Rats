from random import sample
from math import ceil

class Course():
    def __init__(self, course, student_list, class_nr):
        # Give for every course its name, #hoor, max studs werk, max studs prac and the student list for this course
        self.name = course[0]
        self.nr = class_nr
        self.students = random.sample(student_list, len(student_list))
        self.size = len(self.students)
        self.H = []
        self.W = []
        self.P = []

        for nr in range(course[1]):
            self.H.append(Lecture(self.name, f'H{nr + 1}', self.students, self.nr))

        if course[2] > 0:
            self.add_werk(course[2])
        if course[3] > 0:
            self.add_prac(course[3])

    def add_werk(self, max_studs):
        slices = self.make_slices(max_studs)
        for nr in range(len(slices) - 1):
            self.W.append(Lecture(self.name, f'W{nr + 1}', self.students[slices[nr]:slices[nr + 1]], self.nr))

    def add_prac(self, max_studs):
        slices = self.make_slices(max_studs)
        for nr in range(len(slices) - 1):
            self.P.append(Lecture(self.name, f'P{nr + 1}', self.students[slices[nr]:slices[nr + 1]], self.nr))

    def make_slices(self, max_studs):
        rooms = math.ceil(self.size / max_studs)
        min_stud = self.size // rooms
        extra_stud = self.size % rooms

        groups = []
        for nr, room in enumerate(range(rooms)):
            groups.append(min_stud)
            if nr < extra_stud:
                groups[nr] += 1

        slices = [0]
        for nr, group in enumerate(groups):
            slices.append(group + slices[nr])

        return slices
