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

                    with open(f'../data/room{room.name}.yaml', 'w') as file:
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
        '''
        Makes a tuple from an rooster object in the form of:
        ((room.name, slot), (activity.code, (student1.nr, student2.nr, ...)))
        Also sorts it, so small changes still return the same tuple
        '''
        rooster = {}
        # Check all the rooms and timeslots
        for room in self.rooms:
            for slot in np.ndindex(room.rooster.shape):
                act = room.rooster[slot]
                # If the slot is occupied add the activity and its students
                if act != 0:
                    studs = []
                    for stud in act.studs:
                        studs.append(stud.nr)
                        # Sort the students, so the order does not matter
                        studs.sort()
                    rooster[room.name, slot] = (act.code, tuple(studs))
                # If the slot is not occupied put a zero
                else:
                    rooster[room.name, slot] = 0

        # Make a aorted tuple from the dictionary
        return tuple(sorted(rooster.items()))

    def rooster_object(self, rooster_dict):
        '''
        Updates all the students, rooms and activities to get the rooster from
        the given dictionary
        '''
        # Clear the roosters for each student
        for stud in self.students:
            stud.clear_rooster()

        # Loop over all the timeslots in the dictionary
        for slot in list(rooster_dict.items()):
            # Find which room this slot is
            for room in self.rooms:
                if room.name == slot[0][0]:
                    break

            # Check if there is an activity in this slot and room
            if slot[1] != 0:
                # Find the activity this is
                for act in self.activities:
                    if act.code == slot[1][0]:
                        break
                # Make a list of the students in this activity
                studs = []
                for stud in self.students:
                    if stud.nr in slot[1][1]:
                        studs.append(stud)
                # Set the students in this activity to the updated ones
                act.studs = studs
                # Set the activity in the correct slot and room
                room.swap_course(0, act, slot[0][1])
                room.update_malus()
            else:
                # Set the room and slot to 0
                room.rooster[slot[0][1]] = 0
                room.update_malus()

        return self.students, self.rooms, self.activities

    def rooster_per_student(self, output_df):
        """
        Accepts a DataFrame and creates a 5x5 array (rooster) for each unique
        student.
        """
        # Loop over the different students
        for student in output_df['student'].unique():
            rooster_data = output_df[output_df['student'] == student]

            # Create empty rooster
            stud_rooster = np.zeros((5,5), dtype=object)
            # Houd aantal vakken bij
            nr_vakken = 0

            # Create rooster voor deze student
            for _, row in rooster_data.iterrows():
                # Informatie van het in te plannen vak
                vak = row['vak']
                activiteit = row['activiteit']
                zaal = row['zaal']

                day_dict = {'ma': 0, 'di': 1, 'wo': 2, 'do': 3, 'vr': 4, 'za': 5, 'zo': 6}

                # Indices (dag en tijdslot) voor rooster creëren, m.b.v. bovenstaande dict
                dag = row['dag']
                dag_index = day_dict[dag]
                tijdslot = row['tijdslot']
                tijdslot_index = int((tijdslot - 9) / 2)

                # Plak informatie van het in te plannen vak achter elkaar als string
                rooster_data_string = f'{vak}, {activiteit}, {zaal}'

                # Plan vak(ken) als list in op het gewenste moment
                if stud_rooster[tijdslot_index, dag_index] == 0:
                    stud_rooster[tijdslot_index, dag_index] = [rooster_data_string]
                # Meerdere vakken per list in het geval van overlap
                else:
                    stud_rooster[tijdslot_index, dag_index].append(rooster_data_string)

                nr_vakken += 1

        return student, stud_rooster
