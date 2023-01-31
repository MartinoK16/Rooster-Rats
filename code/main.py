import pandas as pd
import numpy as np
import math
import random
import numpy as np
import time
import argparse
import yaml

from student_rooster import *
from classes.rooster import *
from algorithms.evaluation import *
from algorithms.hillclimber import *
from algorithms.initialize import *
from algorithms.tabu_search import *

def main(version, bool):
    courses_df = pd.read_csv('../data/vakken.csv')
    student_df = pd.read_csv('../data/studenten_en_vakken2.csv')
    rooms_df = pd.read_csv('../data/zalen.csv')

    # Rooms with evening timeslot
    evenings = {'C0.110'}

    print('Malus points for version 2, 3 or 4:')

    if version == 1:
        print('This version was just a test fase.')
        print('The versions 2, 3, 4 have implemented algorithms')

    if version == 2:
        my_rooster2 = Rooster(courses_df, student_df, rooms_df, evenings)
        my_rooster2 = Initialize(my_rooster2)
        my_rooster2.make_rooster_random(4, 5, 7)
        malus2 = Evaluation(my_rooster2).malus_count()
        print(f'Malus division version 2: {malus2}')
        print(f'Total malus: {sum(malus2)}')
        # Create output csv
        if bool == 1:
            my_rooster2.make_csv('../data/rooster_v2.csv')

    if version == 3:
        my_rooster3 = Rooster(courses_df, student_df, rooms_df, evenings)
        my_rooster3 = Initialize(my_rooster3)
        my_rooster3.make_rooster_largetosmall()
        malus3 = Evaluation(my_rooster3).malus_count()
        print(f'Malus division version 3: {malus3}')
        print(f'Total malus: {sum(malus3)}')
        # Create output csv
        if bool == 1:
            my_rooster3.make_csv('../data/rooster_v3.csv')

    if version == 4:
        my_rooster4 = Rooster(courses_df, student_df, rooms_df, evenings)
        my_rooster4 = Initialize(my_rooster4)
        my_rooster4.make_rooster_greedy()
        malus4 = Evaluation(my_rooster4).malus_count()
        print(f'Malus division version 3: {malus4}')
        print(f'Total malus: {sum(malus4)}')

        # Create output csv
        if bool == 1:
            my_rooster4.make_csv('../data/rooster_v4.csv')
            output_df_v4 = pd.read_csv('../data/rooster_v4.csv')
            rooster_p_student= Evaluation(my_rooster4).rooster_per_student(output_df_v4)
            print(f'Rooster of last student ({rooster_p_student[0]}):\n{rooster_p_student[1]}')



"""
Create rooster visualisation of all 7 rooms.
1) python -m pip install pdfschedule
2) pip install pyyaml
3) run < pdfschedule --font Courier --color ../data/roomB0.201.yaml ../code/visualisation/roomB0.201.pdf >
in terminal for each different room.
"""


if __name__ == '__main__':
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = 'Run different versions of Rooster')

    # Adding arguments


    parser.add_argument('-v', '--version', type=int, default=5, help='desired rooster version: 2 - 5')
    parser.add_argument('-b', '--bool', type=int, default=0, help='make output false[0] or true[1]')

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.version, args.bool)
