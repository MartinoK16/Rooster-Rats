class Activity():
    def __init__(self, name, type, students, nr, max_studs):
        # Initialize all the required variables
        d = {'L': 1, 'T': 2, 'P': 3}
        self.name = name
        self.type = type
        self.studs = students
        self.code = int(f'{nr + 11}{d[type[0]]}{type[1]}')
        self.size = len(students)
        self.room = None
        self.slot = None
        self.max_studs = max_studs
