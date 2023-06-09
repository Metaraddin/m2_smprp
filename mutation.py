import random


class Mutation(object):
    def __init__(self, mutation_algorithm):
        self.mutation_algorithm = mutation_algorithm

    def mutate(self, population, mutation_probability):
        return self.mutation_algorithm(population, mutation_probability)


class BasicMutation(object):

    def __init__(self):
        pass

    def __call__(self, population, mutation_probability):
        return self.mutate_population(population, mutation_probability)

    # In TSP and QAP problem mutation will have slightly different form. We will choose two genes and swap them.
    @staticmethod
    def mutate_population(population, mutation_probability):
        chromosomes_with_mutated = []

        for chromosome in population:
            if 0 <= random.uniform(0, 1) <= mutation_probability:
                mutated_chromosome = BasicMutation.mutate_chromosome(chromosome,
                                                                     BasicMutation.generate_random_gen_indexes(
                                                                         chromosome))
                chromosomes_with_mutated.append(mutated_chromosome)
            else:
                chromosomes_with_mutated.append(chromosome)

        return chromosomes_with_mutated

    @staticmethod
    def mutate_chromosome(chromosome, random_indexes):
        gen_a_index, gen_b_index = random_indexes
        chromosome[gen_a_index], chromosome[gen_b_index] = chromosome[gen_b_index], chromosome[gen_a_index]
        return chromosome

    @staticmethod
    def generate_random_gen_indexes(chromosome):
        return random.randint(0, len(chromosome) - 1), random.randint(0, len(chromosome) - 1)
