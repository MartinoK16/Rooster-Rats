import argparse
import matplotlib.pyplot as plt

from code.student_rooster import *
from code.classes.rooster import *
from code.algorithms.evaluation import *
from code.algorithms.hillclimber import *
from code.algorithms.initialize import *
from code.algorithms.tabu_search import *
from code.algorithms.simulated_annealing import *
from code.experiments import *

def main(con, iter, csv, yaml, plot):
    if con == '' and iter == '':
        print('Welcome,')
        print('We are Rooster-Rats and we tried to solve the Scheduling problem.')
        print()
        print('You can choose between the following constructive algorithms:')
        print('\t - random (r)')
        print('\t - big-to-small (bs)')
        print('\t - greedy (g)')
        print()
        print('You can choose between the following iterative algorithms:')
        print('\t - hillclimber without students once (hill or h)')
        print('\t - hillclimber without students till no improvements (hill-while or hw)')
        print('\t - hillclimber with students once (hill-stud or hs)')
        print('\t - hillclimber with students till no improvements (hill-stud-while or hsw)')
        print('\t - tabu search (tabu or t)')
        print('\t - simulated annealing (anneal or a)')
        print()
        print("If you chose an iterative algorithm you can plot the malus development by adding: '-plot True'")
        print("You can save the rooster to csv by adding: '-csv True'")
        print("You can save yaml files by adding: '-yaml True'")
        print()
        print('Example:')
        print("python main.py -con 'r' -iter 'hw' -csv True -plot True -yaml True")
        print()
        return

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
        print('Please enter a constructive algorithm')
        return

    elif con == 'random' or con == 'r':
        my_rooster.make_rooster_random(4, 5, 7)

    elif con == 'big-to-small' or con == 'bs':
        my_rooster.make_rooster_largetosmall()

    elif con == 'greedy' or con == 'g':
        my_rooster.make_rooster_greedy()

    else:
        print('Sorry we do not have this constructive algorithm try:')
        print('\t random (r) or')
        print('\t big-to-small (bs) or')
        print('\t greedy (g)')
        return


    # Do a iterative algorithm
    if iter == '':
        print('If you want you can also add an iterative algorithm to improve the rooster')

    elif iter == 'hill' or iter == 'h':
        my_rooster = Hillclimber(my_rooster)
        my_rooster.hc_activities()

    elif iter == 'hill-while' or iter == 'hw':
        my_rooster = Hillclimber(my_rooster)
        prev_malus = sum(Evaluation(my_rooster).malus_count())
        malus = prev_malus - 1
        while malus < prev_malus:
            prev_malus = malus
            my_rooster.hc_activities()
            malus = sum(Evaluation(my_rooster).malus_count())

    elif iter == 'hill-stud' or iter == 'hs':
        my_rooster = Hillclimber(my_rooster)
        my_rooster.hc_activities()
        my_rooster.hc_students('T')
        my_rooster.hc_students('P')

    elif iter == 'hill-stud-while' or iter == 'hsw':
        my_rooster = Hillclimber(my_rooster)
        prev_malus = sum(Evaluation(my_rooster).malus_count())
        malus = prev_malus - 1
        while malus < prev_malus:
            prev_malus = malus
            my_rooster.hc_activities()
            my_rooster.hc_students('T')
            my_rooster.hc_students('P')
            malus = sum(Evaluation(my_rooster).malus_count())

    elif iter == 'tabu' or iter == 't':
        my_rooster = Tabu(my_rooster)
        tabu_list = int(input('How long do you want the tabu list to be? '))
        iters = int(input('How many iterations do you want to do? '))
        my_rooster.tabu_search(tabu_list, iters)

    elif iter == 'anneal' or iter == 'a':
        my_rooster = Simulated_Annealing(my_rooster, 50, 50000)
        my_rooster.run()

    else:
        print('Sorry we do not have this iterative algorithm try:')
        print('\t hill (h) or')
        print('\t hill-while (hw) or ')
        print('\t hill-stud (hs) or')
        print('\t hill-stud-while (hsw) or')
        print('\t tabu (t) or')
        print('\t anneal (a)')


    # Create output csv
    if csv:
        eval = Evaluation(my_rooster)
        malus = sum(eval.malus_count())
        eval.make_csv(f'data/{con}_{iter}_rooster_{malus}_points')
    else:
        print("If you give an extra argument: '-csv True' the rooster will be saved to a csv-file in the data folder")


    # Save yaml files to the data folder
    if yaml:
        Evaluation(my_rooster).make_scheme()
    else:
        print("If you give an extra argument: '-yaml True' a yaml file per room will be made in the data folder")
        print('From each file can then also be made a nice pdf to seen each rooster per room')


    # Make a plot of the development of the malus points of the iterative algorithm
    if iter != '' and plot:
        plt.plot(my_rooster.maluses)
        malus = min(my_rooster.maluses)
        ind = my_rooster.maluses.index(malus)
        plt.plot(ind, malus, markersize=8, marker="o", markerfacecolor="red")
        plt.title(f'Least amount of malus points was {malus} at iteration {ind}')
        plt.xlabel('Iterations')
        plt.ylabel('Malus points')
        plt.grid()
        plt.show()
    elif iter != '':
        print("If you want to see how the malus points develop in the iterative algorithm you can add: '-plot True' as argument")


if __name__ == '__main__':
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = 'Run different versions of Rooster')

    # Adding arguments
    parser.add_argument('-con', '--con', type=str, default='', help='Desired constructive algorithm (default = none)')
    parser.add_argument('-iter', '--iter', type=str, default='', help='Desired iterative algorithm (default = none)')
    parser.add_argument('-csv', '--csv', type=bool, default=False, help='Make csv: True or False (default = False)')
    parser.add_argument('-yaml', '--yaml', type=bool, default=False, help='Make yaml files: True or False (default = False)')
    parser.add_argument('-plot', '--plot', type=bool, default=False, help='Make plot: True or False (default = False)')

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.con, args.iter, args.csv, args.yaml, args.plot)
