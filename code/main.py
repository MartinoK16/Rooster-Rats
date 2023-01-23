import pandas as pd
import numpy as np
import math
import random
import numpy as np
import time
import yaml
import pdfschedule
from classes.rooster import Rooster
from student_rooster import rooster_per_student

courses_df = pd.read_csv('../data/vakken.csv')
student_df = pd.read_csv('../data/studenten_en_vakken2.csv')
rooms_df = pd.read_csv('../data/zalen.csv')

# Rooms with evening timeslot
evenings = {'C0.110'}

print('Malus points for version 2, 3 and 4:')

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
# my_rooster2.make_rooster_minmalus()
my_rooster2.malus_count()
print(my_rooster2.malus) # malus points

# Create output csv
# my_rooster2.make_csv('../data/rooster_v2.csv')

"""
Versie 3: ~900-1000 maluspunten (10000 runs: min = ... / max = ...)

*Indeling van lesuren over tijdsloten – van groot naar klein (lectures & rooms)
*Avondtijdsloten wel geïmplementeerd, maar nog niet gebruikt
*Het benodigde aantal groepen voor de werkcolleges en practica is gemaakt en de groepen worden nog steeds random ingedeeld op basis van de maximum groepsgrootte.
*Maluspunten allemaal toegekend: twee lessen op hetzelfde moment, tussenuren, mensen die niet in een lokaal passen, avondsloten.
*We zorgen ervoor dat iedere student een plekje heeft.
"""
# my_rooster3 = Rooster(courses_df, student_df, rooms_df, evenings)
# my_rooster3.make_rooster_greedy()
# my_rooster3.malus_count()
# print(my_rooster3.malus) # malus points
#
# # Create output csv
# my_rooster3.make_csv('../data/rooster_v3.csv')

"""
Versie 4: ~200-220 maluspunten

*Indeling van lesuren over tijdsloten – van groot naar klein (lectures & rooms) & kijkt welke optie de minste minpunten geeft.
*10 grootste vakken in tijdsloten midden op de dag & in grootste lokaal ingepland.
*Avondtijdsloten wel geïmplementeerd en ook gebruikt.
*Het benodigde aantal groepen voor de werkcolleges en practica is gemaakt en de groepen worden nog steeds random ingedeeld op basis van de maximum groepsgrootte.
*Maluspunten allemaal toegekend: twee lessen op hetzelfde moment, tussenuren, mensen die niet in een lokaal passen, avondsloten.
*We zorgen ervoor dat iedere student een plekje heeft.
"""
# st = time.time()
# my_rooster4 = Rooster(courses_df, student_df, rooms_df, evenings)
# my_rooster4.make_rooster_minmalus()
# my_rooster4.malus_count()
# print(my_rooster4.malus) # malus points
# print(f'Version 4 took {time.time() - st} seconds to run')
#
# # Create output csv
# my_rooster4.make_csv('../data/rooster_v4.csv')


"""
Create rooster per student (as a 5x5 array).
"""
# output_df_v4 = pd.read_csv('../data/rooster_v4.csv')
# rooster_per_student_v4 = rooster_per_student(output_df_v4)

"""
Create rooster visualisation of all 7 rooms.
1) python -m pip install pdfschedule
2) pip install pyyaml
3) run < pdfschedule --font Courier --color ../data/roomB0.201.yaml ../code/visualisation/roomB0.201.pdf >
in terminal for each different room.
"""
<<<<<<< HEAD
for i in range(2):
    my_rooster2.hillclimber_activities()
    my_rooster2.hillclimber_students('W')
    my_rooster2.hillclimber_students('P')
    my_rooster2.hillclimber_students('W')
    my_rooster2.hillclimber_students('P')

# my_rooster2.make_scheme()
# my_rooster2.hillclimber_activities()
#
# for i in range(5):
#     my_rooster2.hillclimber_activities()
#     my_rooster2.hillclimber_students()
#     my_rooster2.hillclimber_students()
#
# my_rooster2.hillclimber_activities()
#
# for i in range(5):
#     my_rooster2.hillclimber_students()
#     my_rooster2.hillclimber_students()
=======
my_rooster2.hillclimber_werk()
my_rooster2.hillclimber_prac()

# my_rooster2.make_scheme()
# for i in range(3):
#     my_rooster2.hillclimber()
#     my_rooster2.hillclimber_werk()
#     my_rooster2.hillclimber_prac()
>>>>>>> 997f0d3 (simulated annealing)
