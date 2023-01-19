class Lecture():
    def __init__(self, lecture_name, lecture_type, lecture_studs, class_nr):
        # Give the lecture its name, type, lecture code and student numbers
        d = {'H': 1, 'W': 2, 'P': 3}
        self.name = lecture_name
        self.type = lecture_type
        self.studs = lecture_studs
        self.code = int(f'{class_nr + 11}{d[lecture_type[0]]}{lecture_type[1]}')
        self.size = len(lecture_studs)
