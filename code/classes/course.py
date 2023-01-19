import random
import math
from .lecture import Lecture

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

        slices = [0]
        for nr in range(rooms):
            if nr < extra_stud:
                slices.append(min_stud + slices[nr] + 1)
            else:
                slices.append(min_stud + slices[nr])

        return slices

# ---------------------------------------------------------------------------------
# def move_werk_students(self): # Same course & lecture_type[0]; different lecture_type[1]
#     groups_dict = {} # dict of lists
#     for werkcollege in self.W:
#         group = werkcollege.type[1]
#         groups_dict[group] = werkcollege.studs # list of students
#
#     return groups_dict
#
#     for group in groups_dict:
#         for student in groups_dict[group]:
#             # Move student
#
#
# def move_prac_students():
#     for practical in self.P:
#         group = practical.type[1]
