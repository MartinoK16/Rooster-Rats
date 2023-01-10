import pandas as pd
import math
import numpy as np
import random

def lecture_count(file):
    df = pd.read_csv(file)

    hoor_dict = {}
    werk_dict = {}
    prac_dict = {}

    for nr, row in df.iterrows():
        for hoor in range(row['#Hoorcolleges']):
            hoor_dict[int(f'{nr + 11}1{hoor + 1}')] = row['Vak'] + f' H{hoor + 1}', row['Verwacht']
        if row['Max. stud. Werkcollege'] > 0:
            for werk in range(math.ceil(row['Verwacht'] / row['Max. stud. Werkcollege'])):
                werk_dict[int(f'{nr + 11}2{werk + 1}')] = row['Vak'] + f' W{werk + 1}', row['Max. stud. Werkcollege']
        if row['Max. stud. Practicum'] > 0:
            for prac in range(math.ceil(row['Verwacht'] / row['Max. stud. Practicum'])):
                prac_dict[int(f'{nr + 11}3{prac + 1}')] = row['Vak'] + f' P{prac + 1}', row['Max. stud. Practicum']

    return dict(sorted(hoor_dict.items(), key=lambda item: item[1][1], reverse=True)), \
            dict(sorted(werk_dict.items(), key=lambda item: item[1][1], reverse=True)), \
            dict(sorted(prac_dict.items(), key=lambda item: item[1][1], reverse=True))

hoor_dict, werk_dict, prac_dict = lecture_count('LecturesLesroosters/vakken.csv')
courses_dict = {**hoor_dict,**werk_dict,**prac_dict}
courses_list = list(courses_dict.keys())

def make_rooster_random(courses_list, hours, days, rooms):
    rooster = np.zeros(hours * days * rooms)
    slots = random.sample(range(hours * days * rooms), len(courses_list))
    for nr, slot in enumerate(slots):
        rooster[slot] = courses_list[nr]
    return rooster.reshape((rooms, hours, days))

room_rooster = make_rooster_random(courses_list, 4, 5, 7)

df = pd.read_csv('LecturesLesroosters/studenten_en_vakken.csv')
df = df.fillna(0)
vakken = []
for _, row in df.iterrows():
    vak = [row['Vak1']]
    if row['Vak2'] != 0:
        vak.append(row['Vak2'])
    if row['Vak3'] != 0:
        vak.append(row['Vak3'])
    if row['Vak4'] != 0:
        vak.append(row['Vak4'])
    if row['Vak5'] != 0:
        vak.append(row['Vak5'])
    vakken.append(set(vak))
df.insert(3, 'Vakken', vakken)
df.replace(0, np.nan, inplace=True)
print(df['Vakken'])
print(df)
df.to_csv('LecturesLesroosters/studenten_en_vakken2.csv')  


def get_output(room_rooster, file):
    df = pd.read_csv(file)
    df['Vakken'] = df['Vak1'] + df['Vak2'] + df['Vak3'] + df['Vak4'] + df['Vak5']
    for room in np.nditer(room_rooster):
        t=1
    #print(df)

get_output(room_rooster, 'LecturesLesroosters/studenten_en_vakken.csv')


def malus_count(df, rooms):
    malus = 0
    # Loop over all the students
    for student in df['student'].unique():
        # Get the dagen and tijdsloten of the student
        rooster = df[df['student'] == student].sort_values(by=['dag', 'tijdslot']).loc[:,('dag', 'tijdslot')]
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
        for room in df['zaal'].unique():
            # Get expected people of the rooms
            expected = df[df['zaal'] == room].sort_values(by=['dag', 'tijdslot']).groupby(['dag', 'tijdslot']).size()
            # Add malus points if the expected value is bigger than the capacity of the room
            malus += max(expected - rooms[room], 0)

    return malus

print(malus_count(df))


#def random_rooster(courses, count_timeslots):
