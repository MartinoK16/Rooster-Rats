def SA_experiment(initial_T=50, nr_runs=10):
    '''
    Accepts two int arguments (initial_T and nr_runs) with default value.
    Creates nr_runs times a greedy rooster and chooses the one with the
    minimum malus points. The Simulated Annealing algorithm is calles on
    this corresponding rooster object, with a variable amount of reheats.
    It returns a list with the best malus points of each SA.
    '''
    # Dict to store the greedy rooster objects with their malus
    random_dict = {}
    for i in range(nr_runs):
        my_rooster = Rooster(courses_df, student_df, rooms_df, evenings)
        my_rooster = Initialize(my_rooster)
        my_rooster.make_rooster_greedy()
        random_dict[my_rooster] = sum(Evaluation(my_rooster).malus_count())

    # Get the best greedy rooster object
    lowest_rooster = min(random_dict, key=random_dict.get)

    # List to store the best malus of each SA
    malus_list_25000 = []
    for j in range(5):
        result = Simulated_Annealing(lowest_rooster, initial_T, 25000).run()
        malus_list_25000.append(result[1])
        print(f'Coördinates minimum: {result[3]}')

        # Plot malus_list
        plt.plot(result[2])

        # Plot min malus in same plot
        plt.plot(result[3][0], result[3][1], markersize=8, marker="o", markerfacecolor="red")
        plt.xlabel('Iteration')
        plt.ylabel('Malus count')
        plt.title('Simulated annealing with 20 reheats')
        plt.savefig(f'plot25000-{result[1]}-{j}.png', dpi=300, bbox_inches='tight')

    print(f'25000{malus_list_25000}')

def make_plot(nr_runs=10, type_rooster='random', algorithm='hc_activities'):
    '''
    Accepts three optional arguments:
    · nr_runs = integer
    · type_rooster = 'random', 'greedy', 'large to small'
    · hc_activities = 'hc_activities', 'hc_students', 'hc_activities_and_students'
    Keeps track of malus count per iteration for each run and creates a lineplot
    of the average, minimum and maximum malus count per iteration.
    '''
    malus_lists = []
    avg_maluses = []
    min_maluses = []
    max_maluses = []

    for i in range(nr_runs):
        my_rooster = Rooster(courses_df, student_df, rooms_df, evenings)
        my_rooster = Initialize(my_rooster)

        if type_rooster == 'random':
            my_rooster.make_rooster_random(4, 5, 7)
        elif type_rooster == 'greedy':
            my_rooster.make_rooster_greedy()
        else:
            my_rooster.make_rooster_largetosmall()

        my_rooster = Hillclimber(my_rooster)

        if algorithm == 'hc_activities':
            my_rooster.hc_activities()
        elif algorithm == 'hc_students':
            my_rooster.hc_students('T')
            my_rooster.hc_students('P')
        else:
            my_rooster.hc_activities()
            my_rooster.hc_students('T')
            my_rooster.hc_students('P')

        malus_lists.append(my_rooster.maluses)

    for j in range(len(malus_lists[0])):
        combine_numbers = [item[j] for item in malus_lists]
        avg_maluses.append(np.mean(combine_numbers))
        min_maluses.append(np.min(combine_numbers))
        max_maluses.append(np.max(combine_numbers))

    plt.fill_between(x=np.linspace(1, 131, num=131), y1=min_maluses, y2=max_maluses, alpha=0.4)
    plt.plot(np.linspace(1, 131, num=131), avg_maluses)
    plt.title(f'Gemiddeld aantal minpunten Hillclimbers (n={nr_runs}) met {type_rooster} beginrooster')
    plt.xlabel('Iteraties')
    plt.ylabel('Aantal minpunten')
    plt.show()

def make_histogram(nr_runs=500, type_rooster='random'):
    '''
    Accepts an integer (nr_runs) and a string (type), which can be 'random' or
    'greedy'. Creates nr_runs times a greedy or random rooster and plots the
    corresponding maluspoints in a histogram.
    '''
    maluses = []
    for i in range(nr_runs):
        my_rooster = Rooster(courses_df, student_df, rooms_df, evenings)
        my_rooster = Initialize(my_rooster)

        if type_rooster == 'random':
            my_rooster.make_rooster_random(4, 5, 7)
        else:
            my_rooster.make_rooster_greedy()
        # print(i)
        malus = sum(Evaluation(my_rooster).malus_count())
        maluses.append(malus)

    print(maluses, min(maluses), max(maluses), np.mean(maluses), np.std(maluses))
    sns.histplot(x=maluses, kde=True)
    plt.title(f'Verdeling minpunten van {nr_runs} {type_rooster} roosters')
    plt.xlabel('Minpunten')
    plt.ylabel('Aantal')
    plt.show()
