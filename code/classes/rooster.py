from .course import *
from .room import *
from .student import *

class Rooster():
    def __init__(self, courses_df, student_df, rooms_df, evenings):
        # Initialize all the required variables
        self.make_students(courses_df, student_df)
        self.make_rooms(rooms_df, evenings)
        self.make_courses(courses_df)
        self.make_activities()

    def make_students(self, courses_df, student_df):
        '''
        Makes a list of students and a dictionary of students per course
        '''
        # Initialize a list for all the student objects
        self.students = []
        # Fill the student_list with student objects
        for _, student in student_df.iterrows():
            self.students.append(Student(student['Stud.Nr.'], 5, 5, student['Vakken']))

        # Initialize a dictionary for lists of student objects per course
        self.student_dict = {}
        # Loop over every course
        for _, course in courses_df.iterrows():
            self.student_dict[course['Vak']] = []
            # Check for every student if they are in this course
            for student in self.students:
                if course['Vak'] in student.courses:
                    self.student_dict[course['Vak']].append(student)

    def make_rooms(self, rooms_df, evenings):
        '''
        Makes a list of room objects based on a DataFrame and sorts them by room capacity
        '''
        self.rooms = []
        # Make the room class for each room from the DataFrame
        for _, row in rooms_df.iterrows():
            self.rooms.append(Room(4, 5, row['Zaalnummber'], row['Zaalnummber'] in evenings, row['Max. capaciteit']))

        # Sort the rooms based on capacity
        self.rooms.sort(key=lambda x: x.capacity, reverse=True)

    def make_courses(self, courses_df):
        '''
        Makes a list of course objects based on a DataFrame and the students which have that course
        '''
        self.courses = []
        # Loop over the courses in the DataFrame
        for nr, row in courses_df.iterrows():
            # Get the required information for this course
            course = [row['Vak'], row['#Hoorcolleges'], row['Max. stud. Werkcollege'], row['Max. stud. Practicum']]
            # Replace NaNs with 0
            course[1:] = [0 if math.isnan(i) else i for i in course[1:]]
            # Make the course class with the students for the course
            self.courses.append(Course(course, self.student_dict[course[0]], nr))

    def make_activities(self):
        '''
        Makes a list of activities objects with first all the lectures sorted on size
        and then the tutorials and practicals sorted on size
        '''
        lec_list = []
        tp_list = []

        # Put all the hoorcolleges in a list
        for course in self.courses:
            for lec in course.L:
                lec_list.append(lec)

        # Put all the tutorials and practicals in a list
        for course in self.courses:
            for tut in course.T:
                tp_list.append(tut)
            for prac in course.P:
                tp_list.append(prac)

        # Sort the list based on the lecture size
        lec_list.sort(key=lambda x: x.size, reverse=True)
        tp_list.sort(key=lambda x: x.size, reverse=True)

        # Add the 2 sorted lists together
        self.activities = lec_list + tp_list
