# KAVIN R V
import random
import numpy as np


def normalize(user_list):
    """
    Normalised with respect to a value got for an ideal scenario
    Value is close to 0.5
    :param user_list:
    :return: Normalised list
    """
    return [((e - 0) / (0.5 - 0)) for e in user_list]


def min_mat(a, b):
    """
    Finds the Y value and calculates Y*T(element wise)
    :param a: X
    :param b: T
    :return: numpy array
    """
    return np.where(a*b > 0, a*b, np.inf).min(1)


def ran_gen(fixed):
    """
    Generate a random chromosomes of random sizes
    :param fixed: Fixed Location
    :return:
    """
    lst = [x for x in range(0, 432) if x not in fixed]
    lst = random.sample(lst, random.randint(0, 37))
    return np.array(lst)


class Genetic:
    def __init__(self, demand, potential, pop_size, mut_rate, travel_time, densities):
        """
        Process the Genetic Algorithm cycle
        :param demand: list of dictionaries containing info about the demand points (Size M)
        :param potential: list of dictionaries containing info about the potential points (Size N)
        :param pop_size: Total Population size (Scalar)
        :param mut_rate: rate at with mutation is processed (Scalar)
        :param travel_time: normalized travel time matrix (numpy Size M x N)
        :param densities: normalized compactness vector (numpy size N)
        """
        self.demand = demand
        self.potential = potential
        self.pop_size = pop_size
        self.mutation_rate = mut_rate/100
        self.travel_time = np.array(travel_time)
        self.densities = densities
        self.population = []
        self.mat_pool = []
        self.fitness = []
        # checks points for fixed and puts their index into a list
        self.fixed = [i for i, x in enumerate(self.potential) if x['Fixed'] == 1]
        self.i = 0

    def gen_population(self):
        """
        Initializes the Population
        :return: None
        """
        a = len(self.population)
        for _ in range(a, self.pop_size):
            self.population.append(ran_gen(self.fixed))

    def gen_full(self, xd):
        """
        Expands each chromosomes to include the fixed locations
        :param xd: the chromosome
        :return: the expanded list as a numpy array
        """
        x = xd.tolist().copy()
        x.extend(self.fitness)
        return np.array(x).astype(int)

    def calc_fitness(self, x2, d, t):
        """
        Calculate the fitness value of a chromosome
        1/(Sum(x[i]*d[i]) + Sum(Y[i, j]*t[i, j])
        :param x2: the chromosome
        :param d: compactness list
        :param t: travel time matrix
        :return: the fitness value
        """
        x = self.gen_full(x2)
        x = [1 if d in x else 0 for d in range(0, 432)]
        x = np.array(x).reshape(len(x), )
        f = 1 / (sum(x * d) + sum(min_mat(x, t)))
        return f

    def eval_fitness(self):
        """
        Evalute fitness for eac chromosome in the population and appends to the class's fitness list
        self.fitness
        :return: None
        """
        self.i += 1
        self.fitness = []
        t = self.travel_time/10
        d = self.densities/10
        for j, x2 in enumerate(self.population):
            f = self.calc_fitness(x2, d, t)
            self.fitness.append(float(f))
        self.fitness = normalize(self.fitness)

    def nat_sel(self):
        """
        Puts each chromosomes into the mating pool multiple times
        Number of times is decided by the value of the fitness
        :return: None
        """
        self.mat_pool = []
        for i, x in enumerate(self.population):
            f = self.fitness[i]
            n = round(f * 100)
            for j in range(n):
                self.mat_pool.append(x)

    def crossover(self, p1, p2):
        """
        Forms new child by choosing random midpoint and combining two parents
        :param p1: Parent 1
        :param p2: Parent 2
        :return: Child as an numpy array
        """
        p1 = p1.tolist()
        p2 = p2.tolist()
        mid_point = min(random.randint(0, len(p1)), random.randint(0, len(p2)))
        child = p1[: mid_point] + p2[mid_point:]
        child = self.mutate(child)
        return np.array(child)

    def new_pop(self):
        """
        Creates new list of population
        :return:
        """
        for i, x in enumerate(self.population):
            p1 = random.choice(self.mat_pool)
            p2 = random.choice(self.mat_pool)
            c1 = self.crossover(p1, p2)
            self.population[i] = c1
        self.eval_fitness()

    def mutate(self, chrom):
        """
        Every gene in the Chromosome has mut_rate% chance to get mutated
        :param chrom: the Chromosome
        :return: mutated Chromosome
        """
        lst = [x for x in range(0, 432) if x not in chrom and x not in self.fixed]
        for i, gene in enumerate(chrom):
            if random.random() < self.mutation_rate:
                chrom[i] = random.choice(lst)

        return chrom

    @property
    def get_best(self):
        """
        :return: Max fitness value, chromosome that contain it(full), without fixed location, total number of facilities
        """
        # self.hubs = [x for x, j in enumerate(self.population[self.fitness.index(max(self.fitness))]) if j == 1]
        k = self.population[self.fitness.index(max(self.fitness))]
        return max(self.fitness), self.gen_full(k), k, len(k) + len(self.fixed)
