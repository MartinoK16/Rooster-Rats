import pandas as pd
import numpy as np
import math
import random
import argparse
import yaml

from student_rooster import *
from classes.rooster import *
from algorithms.evaluation import *
from algorithms.hillclimber import *
from algorithms.initialize import *
from algorithms.tabu_search import *
from experiments import *

try:
    def main(algorithm, csv, plot):
        courses_df = pd.read_csv('../data/vakken.csv')
        student_df = pd.read_csv('../data/studenten_en_vakken2.csv')
        rooms_df = pd.read_csv('../data/zalen.csv')

        # Rooms with evening timeslot
        evenings = {'C0.110'}
        my_rooster = Rooster(courses_df, student_df, rooms_df, evenings)
        my_rooster = Initialize(my_rooster)

        print('Malus points for version 2, 3 or 4:')

        if algorithm == 'random':
            my_rooster.make_rooster_random(4, 5, 7)
            malus = Evaluation(my_rooster).malus_count()
            print(f'Malus division version 2: {malus}')
            print(f'Total malus for: {sum(malus)}')
            # Create output csv

            if csv == 1:
                my_rooster2.make_csv('../data/rooster_random.csv')

            if plot == 1:
                make_histogram(1000, 'random')

        if algorithm == 'greedy':
            my_rooster.make_rooster_greedy()
            malus = Evaluation(my_rooster).malus_count()
            print(f'Malus division version 3: {malus}')
            print(f'Total malus: {sum(malus)}')

            # Create output csv
            if csv == 1:
                my_rooster4.make_csv('../data/rooster_v4.csv')
                output_df_v4 = pd.read_csv('../data/rooster_greedy.csv')
                rooster_p_student= Evaluation(my_rooster4).rooster_per_student(output_df_v4)
                print(f'Rooster of last student ({rooster_p_student[0]}):\n{rooster_p_student[1]}')

            if plot == 1:
                make_histogram(1000, 'greedy')

        if algorithm == 'random hillclimber':
            my_rooster.make_rooster_random(4, 5, 7)
            my_rooster = Hillclimber(my_rooster)
            my_rooster.hc_activities()
            print(Evaluation(my_rooster).malus_count())

            # Create output csv
            if csv == 1:
                my_rooster.make_csv('../data/rooster_random_hillclimber.csv')

            if plot == 1:
                make_plot(nr_runs=10, 'random', 'hc_activities')

        if algorithm == 'greedy hillclimber':
            my_rooster.make_rooster_greedy()
            my_rooster = Hillclimber(my_rooster)
            my_rooster.hc_activities()
            print(Evaluation(my_rooster).malus_count())

            # Create output csv
            if csv == 1:
                my_rooster.make_csv('../data/rooster_greedy_hillclimber.csv')

            if plot == 1:
                make_plot(nr_runs=10, 'greedy', 'hc_activities')

        if algorithm == 'random hillclimber with students':
            my_rooster.make_rooster_random(4, 5, 7)
            my_rooster = Hillclimber(my_rooster)
            my_rooster.hc_activities()
            my_rooster.hc_students('T')
            my_rooster.hc_students('P')
            print(Evaluation(my_rooster).malus_count())

            # Create output csv
            if csv == 1:
                my_rooster.make_csv('../data/rooster_random_hillclimber_stud.csv')

            if plot == 1:
                make_plot(nr_runs=10, 'random', 'hc_activities_and_students')

        if algorithm == 'greedy hillclimber with students':
            my_rooster.make_rooster_greedy()
            my_rooster = Hillclimber(my_rooster)
            my_rooster.hc_activities()
            my_rooster.hc_students('T')
            my_rooster.hc_students('P')
            print(Evaluation(my_rooster).malus_count())

            # Create output csv
            if csv == 1:
                my_rooster.make_csv('../data/rooster_greedy_hillclimber_stud.csv')

            if plot == 1:
                make_plot(nr_runs=10, 'greedy', 'hc_activities_and_students')

        if algorithm == 'greedy simulated annealing':
            my_rooster.make_rooster_greedy()
            Simulated_Annealing(my_rooster, 50, 50000).run()
            print(Evaluation(my_rooster).malus_count())

            # Create output csv
            if csv == 1:
                my_rooster.make_csv('../data/rooster_simulated_annealing.csv')

            if plot == 1:
                SA_experiment()

except:
    print('Welkom,')
    print('We are Rooster-Rats and we tried to solve the Scheduling problem.')
    print('You can choose between the following experiments:')
    print('\t - random')
    print('\t - greedy')
    print('\t - random hillclimber')
    print('\t - greedy hillclimber')
    print('\t - random hillclimber with students')
    print('\t - greedy hillclimber with students')
    print('\t - greedy simulated annealing')

# """
# Create rooster visualisation of all 7 rooms.
# 1) python -m pip install pdfschedule
# 2) pip install pyyaml
# 3) run < pdfschedule --font Courier --color ../data/roomB0.201.yaml ../code/visualisation/roomB0.201.pdf >
# in terminal for each different room.
# """


if __name__ == '__main__':
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = 'Run different versions of Rooster')

    # Adding arguments


    parser.add_argument('-algo', '--algorithm', type=int, default=5, help='desired algorithm')
    parser.add_argument('-csv', '--csv', type=int, default=0, help='make csv false[0] or true[1]')
    parser.add_argument('-plot', '--plot', type=int, default=0, help='make plot false[0] or true[1]')


    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.algorithm, args.csv, args.plot)
