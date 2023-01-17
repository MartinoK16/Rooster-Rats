import numpy as np

# # Output csv naar rooster per student
# output_df = pd.read_csv('../data/rooster_v3.csv')

def rooster_per_student(output_df):
    """
    Accepts a DataFrame and creates a 5x5 array (rooster) for each unique
    student.
    """
    # Loop over the different students
    for student in output_df['student'].unique():
        rooster_data = output_df[output_df['student'] == student]

        # Create empty rooster
        stud_rooster = np.zeros((5,5), dtype=object)
        # Houd aantal vakken bij
        nr_vakken = 0

        # Studentnummer
        # print()
        # print(student)

        # print(rooster_data)

        # Create rooster voor deze student
        for _, row in rooster_data.iterrows():
            # Informatie van het in te plannen vak
            vak = row['vak']
            activiteit = row['activiteit']
            zaal = row['zaal']

            day_dict = {'ma': 0, 'di': 1, 'wo': 2, 'do': 3, 'vr': 4, 'za': 5, 'zo': 6}

            # Indices (dag en tijdslot) voor rooster creëren, m.b.v. bovenstaande dict
            dag = row['dag']
            dag_index = day_dict[dag]
            tijdslot = row['tijdslot']
            tijdslot_index = int((tijdslot - 9) / 2)

            # Plak informatie van het in te plannen vak achter elkaar als string
            rooster_data_string = f'{vak}, {activiteit}, {zaal}'

            # Plan vak(ken) als list in op het gewenste moment
            if stud_rooster[tijdslot_index, dag_index] == 0:
                stud_rooster[tijdslot_index, dag_index] = [rooster_data_string]
            # Meerdere vakken per list in het geval van overlap
            else:
                stud_rooster[tijdslot_index, dag_index].append(rooster_data_string)

            nr_vakken += 1

            # Informatie van het ingeplande vak
            # print(rooster_data_string)

        # Aantal vakken en gemaakte rooster voor deze student
        # print(nr_vakken)
        # print(stud_rooster)
    print()
    print(f'Rooster of last student ({student}):\n{stud_rooster}')
