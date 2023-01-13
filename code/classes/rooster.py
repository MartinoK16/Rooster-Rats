import pandas as pd
import math
import random
import numpy as np

class Rooster():
    def __init__(self, courses_df, student_df, rooms_df):
        self.courses_list = self.make_courses_list(courses_df)
        self.courses = []
        self.make_courses(self.courses_list, student_df)
        self.lectures_list = self.make_lecture_list()
        self.day_dict = {0: 'ma', 1: 'di', 2: 'wo', 3: 'do', 4: 'vr'}
        self.room_dict, self.cap_dict = self.make_room_dict(rooms_df)

    def make_room_dict(self, rooms_df):
        room_dict = {}
        cap_dict = {}
        for nr, row in rooms_df.iterrows():
            room_dict[nr] = row['Zaalnummber'], row['Max. capaciteit']
            cap_dict[row['Zaalnummber']] = row['Max. capaciteit']
        return room_dict, cap_dict

    def make_courses_list(self, df):
        courses_list = []
        for _, row in df.iterrows():
            courses_list.append([row['Vak'], row['#Hoorcolleges'], row['Max. stud. Werkcollege'], row['Max. stud. Practicum']])
        return courses_list

    def make_courses(self, courses_list, student_df):
        # Loop over all the courses needed for the rooster
        for nr, course in enumerate(courses_list):
            # Replace NaN with 0
            course[1:] = [0 if math.isnan(i) else i for i in course[1:]]

            # Loop over the students to see who has this course and add it to the student list
            student_list = []
            for _, student in student_df.iterrows():
                if course[0] in student['Vakken']:
                    student_list.append(student['Stud.Nr.'])

            # Add the course to the rooster
            self.courses.append(Course(course, student_list, nr))

    def make_lecture_list(self):
        lectures = []
        for course in self.courses:
            for hoor in course.H:
                lectures.append(hoor)
        for course in self.courses:
            for werk in course.W:
                lectures.append(werk)
        for course in self.courses:
            for prac in course.P:
                lectures.append(prac)

        return lectures

    def make_rooster_random(self, hours, days, rooms):
        # Make a zeros array with the correct length
        rooster = np.zeros(hours * days * rooms, dtype=object)
        # Get the indices where the lectures will be planned
        slots = random.sample(range(hours * days * rooms), len(self.lectures_list))
        # Put the lecture in the deterimined spot
        for nr, slot in enumerate(slots):
            rooster[slot] = self.lectures_list[nr]
        # Reshape the 1D array to a 3D array for clarity
        self.rooster = rooster.reshape((rooms, hours, days))

    def make_output(self):
        d = {'student': [], 'vak': [], 'activiteit': [], 'zaal': [], 'dag': [], 'tijdslot': []}
        for index in np.ndindex(self.rooster.shape):
            if self.rooster[index] != 0:
                lecture = self.rooster[index]
                for stud in self.rooster[index].studs:
                    d['student'].append(stud)
                    d['vak'].append(lecture.name)
                    d['activiteit'].append(lecture.type)
                    d['zaal'].append(self.room_dict[index[0]][0])
                    d['dag'].append(self.day_dict[index[2]])
                    d['tijdslot'].append(9 + 2 * index[1])

        self.output = pd.DataFrame(data=d)

    def malus_count(self):
        malus = 0
        # Loop over all the students
        for student in self.output['student'].unique():
            # Get the dagen and tijdsloten of the student
            rooster = self.output[self.output['student'] == student].sort_values(by=['dag', 'tijdslot']).loc[:,('dag', 'tijdslot')]
            # Check if there are more than 1 lecture at the same time for this student
            malus += sum(rooster.groupby(['dag', 'tijdslot']).size() - 1)

            # Loop over the days in the students rooster
            for day in rooster['dag'].unique():
                # Get the times of this day
                dag = rooster[rooster['dag'] == day]
                time = dag['tijdslot'].unique()

                # Check if the student has tussenuren
                tussenuur = 0
                if len(time) > 1:
                    for timeslot in range(len(time) - 1):
                        # The rooster is not possible if a student has 3 tussenuren
                        if time[timeslot + 1] - time[timeslot] >= 8:
                            print('Not possible')
                        elif time[timeslot + 1] - time[timeslot] == 6:
                            tussenuur += 2
                        elif time[timeslot + 1] - time[timeslot] == 4:
                            tussenuur += 1
                # If the student has 2 tussenuren it is 3 maluspoints and with 1 tussenuur its 1 maluspoint
                if tussenuur == 2:
                    malus += 3
                elif tussenuur == 1:
                    malus += 1

        # Loop over the different rooms
        for room in self.output['zaal'].unique():
            # Get expected people of the rooms
            expected = self.output[self.output['zaal'] == room].sort_values(by=['tijdslot']).groupby(['dag', 'tijdslot']).size()
            for row in expected - self.cap_dict[room]:
                if row > 0:
                    malus += row

        self.malus = malus
