import numpy as np
import random
from os import system, name
  
class MonteCarlo(object):

    def __init__(self, decay, N, step): 
        self.decay = float(decay) # decay constant
        self.size = int(N) # 2D array size
        self.step = float(step) # time step
        self.decayed = 0 # amount of decayed particles
        self.probability = self.decay * self.step # decay probability
        self.array = np.ones((self.size, self.size), dtype=int) # 2D array full of 1s
        self.decay_time = 0 # decay starting time

    @staticmethod
    def setup(): # ask for user inputs
        return MonteCarlo(input("Enter decay constant (λ): "), input("Enter size of 2D array (N): "), input("Enter time step (Δt): "))

    @staticmethod
    def clear(): # clear chatlog
        if name == 'nt': # for windows 
            _ = system('cls') 
        else: # for mac and linux(here, os.name is 'posix')
            _ = system('clear')

    # compare random number to probability of decay, return if particle decayed
    def has_decayed(self):
        if random.uniform(0, 1) < self.probability:
            self.decayed += 1
            return 0
        else:
            return 1

    # actual half-life calculation
    def half_life(self):
        return np.log(2) / self.decay

    # loop through the 2D array once and check for any new decays
    def loop(self):
        MonteCarlo.clear()
        # formatted visualization of the decay process
        print("------------------------------")
        for x in range(self.size):
            for y in range(self.size):
                # if particle hasn't decayed (1), generate a random number and see if it decays
                if (self.array[x, y] == 1):
                    self.array[x, y] = self.has_decayed()
                print(str(self.array[x, y]) + " ", end='')
            print("")
        print("------------------------------")

    # run the Monte Carlo simulation
    def run(self):
        # keep decaying until the amount has fallen to half of the original amount
        while(self.decayed < self.size ** 2 / 2):
            self.loop()
            # add time step to total decay time
            self.decay_time += self.step

        # final prints
        print("Monte Carlo Simulation Complete!")
        print("------------------------------")
        print("Number of decayed particles: " + str(self.decayed) + " / " + str(self.size ** 2))
        print("Simulated half-life: " + str(self.decay_time))
        print("Actual half-life: " + str(self.half_life()))
        print("------------------------------")

mc = MonteCarlo.setup()
mc.run()
