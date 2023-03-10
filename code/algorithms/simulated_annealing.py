import pandas as pd
from .evaluation import *
from .hillclimber import *
from .initialize import *
import numpy as np
import math
import copy

class Simulated_Annealing():
    def __init__(self, lowest_rooster, initial_T, reheat_point,
     nr_runs=500000, g=0.998):
        self.g = g
        self.nr_runs = nr_runs
        self.initial_T = initial_T
        self.current_T = initial_T
        self.reheat_point = reheat_point
        self.i = 0
        self.rooms = lowest_rooster.rooms
        self.activities = lowest_rooster.activities
        self.courses = lowest_rooster.courses
        self.students = lowest_rooster.students
        self.maluses = []

    def geometric(self):
        '''
        Geometric cooling method
        '''
        self.current_T *= (self.g) ** self.i

    def linear(self, alpha=0.001):
        '''
        Linear cooling method
        '''
        self.current_T -= alpha

    def logarithmic(self):
        '''
        Logarithmic cooling method
        '''
        self.current_T = self.initial_T / (1 + math.log(1 + self.i))

    def exponential(self):
        '''
        Exponential cooling method
        '''
        self.current_T = max(0.05, self.current_T * self.g)

    def run(self):
        '''
        This function applies the simulated annealing algorithm,
        where it declines a lecture swap with a random
        chance > e ^ (delta / T). It cools down via one of the
        called cooling methods above. The lecture swap swaps two
        randomly chosen lectures. It saves the malus for each rooster
        and it returns the best rooster with best malus.
        '''
        prev_malus = sum(Evaluation(self).malus_count())
        self.best = Evaluation(self).rooster_dict()

        while self.i < self.nr_runs:
            self.i += 1
            # Random room and slot from activities
            lecture1 = random.choice(self.activities)
            room1 = lecture1.room
            slot1 = lecture1.slot

            # Room2 could also be an empty room
            slots = []
            room2 = random.choice(self.rooms)
            for slot in np.ndindex(room2.rooster.shape):
                slots.append(slot)
            slot2 = random.choice(slots)
            lecture2 = room2.rooster[slot2]

            # Malus before swap
            old = sum(Evaluation(self).malus_count())

            # Swapping lectures
            Hillclimber(self).swap_course(room1, lecture1, slot1, room2, lecture2, slot2)

            # Malus after swap
            new = sum(Evaluation(self).malus_count())

            # Decline swap with delta > 50 or random chance
            if new > old + 50 or random.uniform(0, 1) > round(math.exp((old-new) / self.current_T),10):
                Hillclimber(self).swap_course(room1, lecture2, slot1, room2, lecture1, slot2)

            # Apply cooling method
            self.exponential()

            # Reheat when neccessary
            if self.i % self.reheat_point == 0:
                self.current_T += 5

            # Add malus to list
            malus = sum(Evaluation(self).malus_count())
            self.maluses.append(malus)
            print(malus, "\t", self.current_T)

            if malus < prev_malus:
                prev_malus = malus
                self.best = Evaluation(self).rooster_dict()

        # Get rooster with lowest malus
        self.students, self.rooms, self.activities = Evaluation(self).rooster_object(dict(self.best))
