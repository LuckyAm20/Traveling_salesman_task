import random
from random import random, sample, shuffle, randint

from deap import base, creator, tools

from algorithms.utils.path import Path

from .utils.calculator import Calculator


class GA:
    def __init__(self, population, iterations, selection_coef, mutation_coef, a, b, N, M):
        self.population = population
        self.iterations = iterations
        self.selection_coef = selection_coef
        self.mutation_coef = mutation_coef
        self.a = a
        self.b = b
        self.N = N
        self.M = M

        self.toolbox = base.Toolbox()
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        self.toolbox.register("individual", self.generate_individual)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        self.toolbox.register("mate", self.__crossover)
        self.toolbox.register("mutate", self.__mutation)
        self.toolbox.register("select", tools.selBest)

    def generate_individual(self):
        base_1 = list(range(self.N))
        base_2 = list(range(self.N, self.M + self.N))
        shuffle(base_1)
        shuffle(base_2)
        individual = base_1[:self.a] + base_2[:self.b] + [base_1[0]]
        return creator.Individual(individual)

    def __crossover(self, individuals: list[list[int]]) -> None:
        childs = []
        w_size = len(individuals[0]) // 4
        for _ in range(self.population):
            p1, p2 = sample(individuals, 2)
            p1_a = list({x for x in p1 if x in list(range(self.N))})
            p1_b = list({x for x in p1 if x in list(range(self.N, self.M + self.N))})
            p2_a = list({x for x in p2 if x in list(range(self.N))})
            p2_b = list({x for x in p2 if x in list(range(self.N, self.M + self.N))})
            childs.append(creator.Individual(
                p1_a + p2_b + [p1_a[0]])
            )
        return childs

    def __mutation(self, individuals: list[list[int]]) -> None:
        sampling = list(range(1, len(individuals[0]) - 1))
        for item in individuals:
            if random() < self.mutation_coef:
                for _ in range(randint(len(item), len(item) * 4)):
                    i, j = sample(sampling, 2)
                    item[i], item[j] = item[j], item[i]

    def run(self, points, name=None):
        l = len(points)
        dm = Calculator.calculate_distance_matrix([x[0] for x in points])

        population = self.toolbox.population(n=self.population)

        for _ in range(self.iterations):
            population_1 = population.copy()
            offspring_1 = self.toolbox.mate(population)

            self.toolbox.mutate(offspring_1)
            self.toolbox.mutate(population_1)
            offspring_2 = self.toolbox.mate(population)

            fits = [(ind, Calculator.calculate_path_length(dm, ind)) for ind in
                    offspring_1 + offspring_2 + population_1]

            for ind, fit in fits:
                ind.fitness.values = (fit,)

            population = self.toolbox.select(offspring_1 + offspring_2 + population + population_1, k=self.population)

        best_ind = tools.selBest(population, 1)[0]
        return Path(indexes=best_ind, length=Calculator.calculate_path_length(dm, best_ind), name=name)
