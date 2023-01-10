import pandas as pd
import math
import numpy as np

def lecture_count(file):
    df = pd.read_csv(file)

    # Get the total amount of hoorcolleges rooms needed
    hoor_count = df.sum(axis=0)[1]

    werk_count = 0
    prac_count = 0
    courses_list = []
    # Loop over the vakken and count the number of werkcolleges and practica rooms needed
    for _, row in df.iterrows():
        for hoor in range(row['#Hoorcolleges']):
            # If there are werkcolleges then add the correct amount of rooms to the total
            courses_list.append(row['Vak'] + f' H{hoor + 1}')
        if row['#Werkcolleges'] > 0:
            # If there are werkcolleges then add the correct amount of rooms to the total
            count = math.ceil(row['Verwacht'] / row['Max. stud. Werkcollege'])
            werk_count += count
            for werk in range(count):
                courses_list.append(row['Vak'] + f' W{werk + 1}')
        if row['#Practica'] > 0:
            # If there are practica then add the correct amount of rooms to the total
            count = math.ceil(row['Verwacht'] / row['Max. stud. Practicum'])
            prac_count += count
            for prac in range(count):
                courses_list.append(row['Vak'] + f' P{prac + 1}')

    return courses_list, hoor_count, werk_count, prac_count

courses_list, hoor_count, werk_count, prac_count = lecture_count('LecturesLesroosters/vakken.csv')
print(courses_list)


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
