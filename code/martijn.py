import random
import math
import pandas as pd
import numpy as np

from classes import Rooster, Course, Lecture

# Martijn

my_rooster = Rooster(courses_df, student_df, rooms_df)
my_rooster.make_rooster_random(4, 5, 7)
print(my_rooster.rooster)
my_rooster.make_output()
print(my_rooster.output)
my_rooster.output.to_csv('data/test.csv')
my_rooster.malus_count()
print(my_rooster.malus)
