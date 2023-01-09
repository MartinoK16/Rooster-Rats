import pandas as pd
import math
import numpy as np

def lecture_count(file):
    df = pd.read_csv(file)

    # Get the total amount of hoorcolleges rooms needed
    hoor_count = df.sum(axis=0)[1]

    werk_count = 0
    prac_count = 0
    # Loop over the vakken and count the number of werkcolleges and practica rooms needed
    for _, row in df.iterrows():
        if row['#Werkcolleges'] > 0:
            # If there are werkcolleges then add the correct amount of rooms to the total
            werk_count += math.ceil(row['Verwacht'] / row['Max. stud. Werkcollege'])
        if row['#Practica'] > 0:
            # If there are practica then add the correct amount of rooms to the total
            prac_count += math.ceil(row['Verwacht'] / row['Max. stud. Practicum'])

    return hoor_count, werk_count, prac_count

counts = lecture_count('LecturesLesroosters/vakken.csv')
print(counts)


def malus_count(df, rooms):
    malus = 0
    # Loop over all the students
    for student in df['student'].unique():
        # Get the dagen and tijdsloten of the student
        rooster = df[df['student'] == student].sort_values(by=['dag', 'tijdslot']).loc[:,('dag', 'tijdslot')]
        #print(rooster.groupby(['dag', 'tijdslot']).size())
        # Check if there are more than 1 lecture at the same time
        malus += sum(rooster.groupby(['dag', 'tijdslot']).size() - 1)

        for day in rooster['dag'].unique():
            dag = rooster[rooster['dag'] == day]
            time = dag['tijdslot'].unique()
            print(time)
            tussenuur = 0
            if len(time) > 1:
                for timeslot in range(len(time) - 1):
                    if time[timeslot + 1] - time[timeslot] >= 8:
                        print('Not possible')
                    elif time[timeslot + 1] - time[timeslot] == 6:
                        tussenuur += 2
                    elif time[timeslot + 1] - time[timeslot] == 4:
                        tussenuur += 1
            if tussenuur == 2:
                malus += 3
            elif tussenuur == 1:
                malus += 1

        for room in df['zaal'].unique():
            # Get expected people of the rooms
            expected = df[df['zaal'] == room].sort_values(by=['dag', 'tijdslot']).groupby(['dag', 'tijdslot']).size()
            malus += max(expected - rooms[room], 0)

    return malus

df = pd.DataFrame([[9, 9, 9, 9, 11, 13, 17, 11, 15, 9, 11, 13, 9, 13, 17], list('AAAABBABABCBDDD'), [1.1, 1.7, 1.8, 2.5, 2.6, 3.3, 3.8,4.0,4.2,4.3,4.5,4.6,4.7,4.7,4.8], ['x/y/z','x/y','x/y/z/n','x/u','x','x/u/v','x/y/z','x','x/u/v/b','-','x/y','x/y/z','x','x/u/v/w', 'x'],['1','3','3','3','2','4','2','5','3','6','3','5','1','1','1']]).T
df.columns = ['tijdslot','student','col3','col4','dag']

print(malus_count(df))
