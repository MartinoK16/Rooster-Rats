import pandas as pd
import numpy as np
import yaml

class Evaluation():
    def __init__(self, rooster):
        self.rooms = rooster.rooms
        self.courses = rooster.courses
        self.students = rooster.students
        self.activities = rooster.activities

    def make_csv(self, filename):
        '''
        This function makes a DataFrame with the required columns for the output
        and saves it to a csv-file.
        '''
        # Mapping dictionaries
        day_dict = {0: 'mon', 1: 'tue', 2: 'wed', 3: 'thu', 4: 'fri'}
        time_dict = {0: 9, 1: 11, 2: 13, 3: 15, 4: 17}

        # Empty dictionary to store all the information
        d = {'student': [], 'course': [], 'activity': [], 'room': [], 'day': [], 'timeslot': []}

        for room in self.rooms:
            # Loop over every timeslot for this room
            for slot in np.ndindex(room.rooster.shape):
                # Check if there is a lecture
                if room.rooster[slot] != 0:
                    # Add all the students for this lecture to dictionary
                    lecture = room.rooster[slot]
                    for stud in lecture.studs:
                        d['student'].append(stud.nr)
                        d['course'].append(lecture.name)
                        d['activity'].append(lecture.type)
                        d['room'].append(room.name)
                        d['day'].append(day_dict[slot[1]])
                        d['timeslot'].append(time_dict[slot[0]])

        # Save the DataFrame as csv with the given filename/path
        pd.DataFrame(data=d).to_csv(filename)

    def make_scheme(self):
        '''

        '''
        day_dict_scheme = {0: 'M', 1: 'T', 2: 'W', 3: 'R', 4: 'F'}
        for room in self.rooms:
            dict = {'name': [], 'days': [], 'time': []}
            for slot in np.ndindex(room.rooster.shape):
                if room.rooster[slot] != 0:
                    lecture = room.rooster[slot]
                    dict['name'].append(f'{lecture.name}, type: {lecture.type}, size: {lecture.size}')
                    dict['days'].append(day_dict_scheme[slot[1]])
                    dict['time'].append(f'{9 + 2 * slot[0]} - {+ 11 + 2 * slot[0]}')

                    df = pd.DataFrame(data=dict)

                    with open(f'../data/room{room.room}.yaml', 'w') as file:
                        documents = yaml.dump(df.to_dict(orient='records'), file, default_flow_style=False)

    def malus_count(self):
        self.malus = [0, 0, 0, 0]
        for student in self.students:
            self.malus[0] += student.malus[0]
            self.malus[1] += student.malus[1]
        for room in self.rooms:
            self.malus[2] += room.malus[0]
            self.malus[3] += room.malus[1]
        return self.malus

    def rooster_dict(self):
        rooster = {}
        for room in self.rooms:
            for slot in np.ndindex(room.rooster.shape):
                act = room.rooster[slot]
                if act != 0:
                    studs = []
                    for stud in act.studs:
                        studs.append(stud.nr)
                    rooster[room.name, slot] = (act.code, tuple(studs))
                else:
                    rooster[room.name, slot] = 0
        return rooster

    def rooster_object(self, rooster_dict):
        for stud in self.students:
            stud.clear_rooster()

        for slot in list(rooster_dict.items()):
            for room in self.rooms:
                if room.name == slot[0][0]:
                    break

            if slot[1] != 0:
                for act in self.activities:
                    if act.code == slot[1][0]:
                        break

                studs = []
                for stud in self.students:
                    if stud.nr in slot[1][1]:
                        studs.append(stud)

                act.studs = studs
                room.swap_course(0, act, slot[0][1])
            else:
                room.rooster[slot[0][1]] = 0
                room.update_malus()
                
        return self
