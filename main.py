import argparse

from code.student_rooster import *
from code.classes.rooster import *
from code.algorithms.evaluation import *
from code.algorithms.hillclimber import *
from code.algorithms.initialize import *
from code.algorithms.tabu_search import *
from code.algorithms.simulated_annealing import *
from code.experiments import *

def main(con, iter, csv, plot):
    courses_df = pd.read_csv('data/vakken.csv')
    student_df = pd.read_csv('data/studenten_en_vakken.csv')
    rooms_df = pd.read_csv('data/zalen.csv')

    # Rooms with evening timeslot
    evenings = {'C0.110'}

    # Initialize rooster object
    my_rooster = Rooster(courses_df, student_df, rooms_df, evenings)
    my_rooster = Initialize(my_rooster)


    # Do a constructive initialization
    if con == '':
        pass

    elif con == 'random' or con == 'r':
        my_rooster.make_rooster_random(4, 5, 7)

    elif con == 'greedy' or con == 'g':
        my_rooster.make_rooster_greedy()

    else:
        print('Sorry we do not have this constructive algorithm try:')
        print('\t random (r) or')
        print('\t greedy (g)')
        print()


    # Do a iterative algorithm
    if iter == '':
        pass

    elif iter == 'hill' or iter == 'h':
        my_rooster = Hillclimber(my_rooster)
        my_rooster.hc_activities()

    elif iter == 'hill-stud' or iter == 'hs':
        my_rooster = Hillclimber(my_rooster)
        my_rooster.hc_activities()
        my_rooster.hc_students('T')
        my_rooster.hc_students('P')

    elif iter == 'tabu' or iter == 't':
        my_rooster = Tabu(my_rooster)
        my_rooster.tabu_search(100, 10000)

    elif iter == 'anneal' or iter == 'a':
        my_rooster = Simulated_Annealing(my_rooster, 50, 50000)
        my_rooster.run()

    else:
        print('Sorry we do not have this iterative algorithm try:')
        print('\t hill (h) or')
        print('\t hill-stud (hs) or')
        print('\t tabu (t) or')
        print('\t anneal (a)')

    # if algorithm == 'greedy simulated annealing':
    #     my_rooster.make_rooster_greedy()
    #     Simulated_Annealing(my_rooster, 50, 50000).run()
    #     print(Evaluation(my_rooster).malus_count())
    #
    #     # Create output csv
    #     if csv == 1:
    #         my_rooster.make_csv('../data/rooster_simulated_annealing.csv')
    #
    #     if plot == 1:
    #         SA_experiment()


    # Create output csv
    if csv:
        eval = Evaluation(my_rooster)
        malus = sum(eval.malus_count())
        eval.make_csv(f'data/{con}_{iter}_rooster_{malus}_points')

    if plot:
        make_histogram(1000, 'greedy')



# """
# Create rooster visualisation of all 7 rooms.
# 1) python -m pip install pdfschedule
# 2) pip install pyyaml
# 3) run < pdfschedule --font Courier --color ../data/roomB0.201.yaml ../code/visualisation/roomB0.201.pdf >
# in terminal for each different room.
# """

print('Welkom,')
print('We are Rooster-Rats and we tried to solve the Scheduling problem.')
print('You can choose between the following constructive algorithms:')
print('\t - random (r)')
print('\t - greedy (g)')
print()
print('You can choose between the following iterative algorithms:')
print('\t - hillclimber without students (hill or h)')
print('\t - hillclimber with students (hill-stud or hs)')
print('\t - tabu search (tabu or t)')
print('\t - simulated annealing (anneal or a)')
print()

if __name__ == '__main__':
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = 'Run different versions of Rooster')

    # Adding arguments
    parser.add_argument('-con', '--con', type=str, default='', help='Desired constructive algorithm (default = none)')
    parser.add_argument('-iter', '--iter', type=str, default='', help='Desired iterative algorithm (default = none)')
    parser.add_argument('-csv', '--csv', type=bool, default=False, help='Make csv: True or False (default = False)')
    parser.add_argument('-plot', '--plot', type=bool, default=False, help='Make plot: True or False (default = False)')

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.con, args.iter, args.csv, args.plot)
