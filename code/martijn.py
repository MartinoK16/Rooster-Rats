import pandas as pd

from classes.rooster import Rooster

# Martijn

courses_df = pd.read_csv('data/vakken.csv')
student_df = pd.read_csv('data/studenten_en_vakken2.csv')
rooms_df = pd.read_csv('data/zalen.csv')

# my_course = Course('Hey', [1], 5)
my_rooster = Rooster(courses_df, student_df, rooms_df)
my_rooster.make_rooster_random(4, 5, 7)
print(my_rooster.rooster)
my_rooster.make_output()
print(my_rooster.output)
my_rooster.output.to_csv('data/test.csv')
my_rooster.malus_count()
print(my_rooster.malus)
