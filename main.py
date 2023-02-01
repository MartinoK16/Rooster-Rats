import argparse
import matplotlib.pyplot as plt

from code.student_rooster import *
from code.classes.rooster import *
from code.algorithms.evaluation import *
from code.algorithms.hillclimber import *
from code.algorithms.initialize import *
from code.algorithms.tabu_search import *
from code.algorithms.simulated_annealing import *

def main(con, iter, csv, yaml, plot):
    if con == '' and iter == 'none':
        print('Welcome,')
        print('We are Rooster-Rats and we tried to solve the Scheduling problem.')
        print()
        print('You can choose between the following constructive algorithms:')
        print('\t - random (r)')
        print('\t - big-to-small (bs)')
        print('\t - greedy (g)')
        print()
        print('You can choose between the following iterative algorithms:')
        print('\t - hillclimber (hill or h)')
        print('\t - tabu search (tabu or t)')
        print('\t - simulated annealing (anneal or a)')
        print()
        print("If you chose an iterative algorithm you can plot the malus development by adding: -plot 'y'")
        print("You can save the rooster to csv by adding: -csv 'y'")
        print("You can save yaml files by adding: -yaml 'y'")
        print('If you do not add these arguments it will be asked after making the rooster')
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


    # Do an iterative algorithm
    if iter == 'none':
        print('If you want you can also add an iterative algorithm to improve the rooster')

    # Hillclimber
    elif iter == 'hill' or iter == 'h':
        my_rooster = Hillclimber(my_rooster)
        do_while = input('Do you want to loop till no improvement? [y/n] ')
        do_studs = input('Do you want to include student swaps? [y/n] ')

        # With while loop
        if do_while == 'y':
            prev_malus = sum(Evaluation(my_rooster).malus_count())
            malus = prev_malus - 1

            while malus < prev_malus:
                prev_malus = malus
                my_rooster.hc_activities()

                # With student swaps
                if do_studs == 'y':
                    my_rooster.hc_students('T')
                    my_rooster.hc_students('P')

                malus = sum(Evaluation(my_rooster).malus_count())

        # Without while loop
        else:
            my_rooster.hc_activities()
            # With student swaps
            if do_studs == 'y':
                my_rooster.hc_students('T')
                my_rooster.hc_students('P')

    # Tabu Search
    elif iter == 'tabu' or iter == 't':
        my_rooster = Tabu(my_rooster)

        iters = input('How many iterations do you want to do? [int] ')
        list_len = input('How long do you want the tabu list to be? [int] ')

        if iters == '' or iters == 'd':
            iters = 1000
        if list_len == '' or list_len == 'd':
            list_len = 100

        my_rooster.tabu_search(int(list_len), int(iters))

    # Simulated Annealing
    elif iter == 'anneal' or iter == 'a':
        iters = input('How many iterations do you want to do? [int] ')
        start_temp = input('What do you want the start temperature to be? [int] ')
        reheat_iter = input('After how many iterations do you want to reheat? [int] ')

        if iters == '' or iters == 'd':
            iters = 500000
        if start_temp == '' or start_temp == 'd':
            start_temp = 50
        if reheat_iter == '' or reheat_iter == 'd':
            reheat_iter = 50000

        my_rooster = Simulated_Annealing(my_rooster, int(start_temp), int(reheat_iter), nr_runs=int(iters))
        my_rooster.run()

    else:
        print('Sorry we do not have this iterative algorithm try:')
        print('\t hill (h) or')
        print('\t tabu (t) or')
        print('\t anneal (a)')


    # Create output csv
    if csv == 'n':
        pass
    elif csv != 'y':
        csv = input('Do you want to save this rooster to a csv-file? [y/n] ')

    if csv == 'y':
        eval = Evaluation(my_rooster)
        malus = sum(eval.malus_count())
        eval.make_csv(f'data/{con}_{iter}_rooster_{malus}_points')

    # Save yaml files to the data folder
    if yaml == 'n':
        pass
    elif yaml != 'y':
        yaml = input('Do you want to save yaml-files of this rooster? [y/n] ')

    if yaml == 'y':
        Evaluation(my_rooster).make_scheme()

    # Make a plot of the development of the malus points of the iterative algorithm
    if iter != '':
        if plot == 'n':
            pass
        elif plot != 'y':
            plot = input('Do you want plot and save the development of the malus points? [y/n] ')

        if plot == 'y':
            plt.plot(my_rooster.maluses)
            malus = min(my_rooster.maluses)
            ind = my_rooster.maluses.index(malus)
            plt.plot(ind, malus, markersize=8, marker="o", markerfacecolor="red")
            plt.title(f'Least amount of malus points was {malus} at iteration {ind}')
            plt.xlabel('Iterations')
            plt.ylabel('Malus points')
            plt.grid()

            mng = plt.get_current_fig_manager()
            mng.full_screen_toggle()
            plt.savefig(f'{con}_{iter}_malus_development_{malus}_points.png')
            mng.full_screen_toggle()

            plt.show()

if __name__ == '__main__':
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = 'Run different versions of Rooster')

    # Adding arguments
    parser.add_argument('-con',  '--con',  type=str, default='', help='Desired constructive algorithm')
    parser.add_argument('-iter', '--iter', type=str, default='none', help='Desired iterative algorithm')
    parser.add_argument('-csv',  '--csv',  type=str, default='', help='Save csv [y/n]')
    parser.add_argument('-yaml', '--yaml', type=str, default='', help='Save yamls [y/n]')
    parser.add_argument('-plot', '--plot', type=str, default='', help='Save plot [y/n]')

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.con, args.iter, args.csv, args.yaml, args.plot)
