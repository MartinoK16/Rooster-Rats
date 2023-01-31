def SA_experiment(initial_T=50, nr_runs=10):
    '''
    Accepts an integer (nr_runs) and a string (type), which can be 'random' or
    'greedy'. Creates nr_runs times a greedy or random rooster and plots the
    corresponding maluspoints in a histogram.
    '''
    random_dict = {}
    reheat_list = [5000, 10000, 20000, 25000, 50000]
    malus_list = []
    for i in range(nr_runs):
        my_rooster = Rooster(courses_df, student_df, rooms_df, evenings)
        my_rooster = Initialize(my_rooster)
        my_rooster.make_rooster_greedy()
        malus = sum(Evaluation(my_rooster).malus_count())
        random_dict[my_rooster] = malus

    lowest_rooster = min(random_dict, key=random_dict.get)

    # for j in range(6):
    #     for heat in reheat_list:
    start = time.time()
    result = Simulated_Annealing(lowest_rooster, initial_T, 50000).run()
    sa_rooster = result[0]
    malus_list.append(result[1])
    stop = time.time()
    print(f'Runtime for simulated annealing is : {stop-start}')
    #print(j, malus_list)

    return malus_list
