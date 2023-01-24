import random
import math
from .activity import Activity

class Course():
    def __init__(self, course, students, nr):
        # Initialize all the required variables
        self.name = course[0]
        self.nr = nr
        self.students = random.sample(students, len(students))
        self.size = len(self.students)
        self.L = []
        self.T = []
        self.P = []

        # Add the lectures
        for nr in range(course[1]):
            self.L.append(Activity(self.name, f'L{nr + 1}', self.students, self.nr, self.size))

        # Add the tutorials if there are any
        if course[2] > 0:
            self.add_small_activity(course[2], 'T')
        # Add the practicals if there are any
        if course[3] > 0:
            self.add_small_activity(course[3], 'P')

    def add_small_activity(self, max_studs, TorP):
        '''
        Get the correct groups to make tutorials
        '''
        # Get the groups
        slices = self.make_slices(max_studs)
        # Add the activities with the correct number of people
        for nr in range(len(slices) - 1):
            getattr(self, TorP).append(Activity(self.name, f'{TorP}{nr + 1}', self.students[slices[nr]:slices[nr + 1]], self.nr, max_studs))

    def make_slices(self, max_studs):
        '''
        Makes as even groups as possible from the max amount of students allowed
        and number of students of the course
        '''
        # Calculate neccisarry values
        rooms = math.ceil(self.size / max_studs)
        min_stud = self.size // rooms
        extra_stud = self.size % rooms

        slices = [0]
        # Loop over the amount of rooms needed and make the correct groups
        for nr in range(rooms):
            if nr < extra_stud:
                slices.append(min_stud + slices[nr] + 1)
            else:
                slices.append(min_stud + slices[nr])

        return slices
