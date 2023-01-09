import pandas as pd
import math

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
