import pandas as pd
import math
import random
import numpy as np
from classes.course import Course
from classes.room import Room
from classes.student_rooster import rooster_per_student

courses_df = pd.read_csv('data/vakken.csv')
student_df = pd.read_csv('data/studenten_en_vakken2.csv')
rooms_df = pd.read_csv('data/zalen.csv')

# Rooms with evening timeslot
evenings = {'C0.110REMOVE'}

"""
Versie 1: ~4500 maluspunten
*Random indeling van lesuren over tijdsloten.
*Avondtijdsloten niet geïmplementeerd.
*Geen rekening gehouden met maximum groepsgrootte van werkcolleges en practica bij de indeling, hier ook geen maluspunten aan toegekend. Echter, wel het benodigde
 aantal groepen gemaakt en iedere student aan elk van deze groepen toegevoegd.
*Maluspunten allemaal toegekend: twee lessen op hetzelfde moment, tussenuren, mensen die niet in een lokaal passen, avondsloten.
*Niet meerdere lessen in 1 lokaal op hetzelfde moment. 😊
"""

"""
Versie 2: ~1300-1800 maluspunten (10000 runs: min = 1194 / max = 2115)
*Random indeling van lesuren over tijdsloten.
*Avondtijdsloten niet geïmplementeerd.
*Wel rekening gehouden met maximum groepsgrootte bij de indeling, hier ook maluspunten aan toegekend. Het benodigde aantal groepen is gemaakt voor werkcolleges en
 practica en deze groepen worden random ingedeeld op basis van de maximum groepsgrootte.
*Gelijke groepen voor de werkgroepen en practicagroepen.
*Maluspunten allemaal toegekend: twee lessen op hetzelfde moment, tussenuren, mensen die niet in een lokaal passen, avondsloten.
"""
my_rooster2 = Rooster(courses_df, student_df, rooms_df, evenings)
my_rooster2.make_rooster_random(4, 5, 7) # timeslots, # days, # rooms
my_rooster2.malus_count()
print(my_rooster2.malus) # malus points

# Create output csv
my_rooster2.make_csv('data/rooster_v2.csv')

"""
Versie 3: ~900-1000 maluspunten (10000 runs: min = ... / max = ...)
*Indeling van lesuren over tijdsloten – van groot naar klein (lectures & rooms)
*Avondtijdsloten wel geïmplementeerd, maar nog niet gebruikt
*Het benodigde aantal groepen voor de werkcolleges en practica is gemaakt en de groepen worden nog steeds random ingedeeld op basis van de maximum groepsgrootte.
*Maluspunten allemaal toegekend: twee lessen op hetzelfde moment, tussenuren, mensen die niet in een lokaal passen, avondsloten.
"""
my_rooster3 = Rooster(courses_df, student_df, rooms_df, evenings)
my_rooster3.make_rooster_greedy()
my_rooster3.malus_count()
print(my_rooster3.malus) # malus points

# Create output csv
my_rooster3.make_csv('data/rooster_v3.csv')

"""
Create rooster per student (as a 5x5 array)
"""
output_df_v3 = pd.read_csv('data/rooster_v3.csv')
rooster_per_student_v3 = rooster_per_student(output_df_v3)
