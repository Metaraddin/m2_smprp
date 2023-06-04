import time

import numpy as np
from scipy.optimize import quadratic_assignment

from fitness import compute_fitness_scores_list, compute_fitness_scores, get_normalized_result_of_fitness_function_scores_list
from population import generate_random_population
from mutation import Mutation, BasicMutation
from selection import Selection, TournamentSelection
from crossover import BasicCrossover, Crossover

selection_strategy = Selection(selection_algorithm=TournamentSelection())
mutation_strategy = Mutation(mutation_algorithm=BasicMutation())
crossover_strategy = Crossover(crossover_algorithm=BasicCrossover())


def assignement_problem_ga(distance_matrix, 
                           flow_matrix, 
                           **params):
    population = generate_random_population(distance_matrix.shape[0], params['population_size'])
    
    # generation_indices = []
    # average_results = []
    # min_results = []
    # max_results = []
    previous_max_chromosome = []
    max_chromosome = None
    generations_no_improve = 0

    start = time.time()

    for epoch in range(params['number_of_generations']):
        fitness_scores = compute_fitness_scores_list(population, distance_matrix, flow_matrix)
        fitness_scores_normalized = get_normalized_result_of_fitness_function_scores_list(fitness_scores)

        max_fitness = np.min(fitness_scores)
        # min_fitness = np.max(fitness_scores)
        average_fitness = np.mean(fitness_scores)

        # max_results.append(max_fitness)
        # min_results.append(min_fitness)
        # average_results.append(average_fitness)
        # generation_indices.append(epoch)

        max_chromosome = population[np.argmin(fitness_scores)]
        max_chromosome = list(map(lambda value: value + 1, max_chromosome))

        selected_chromosomes = selection_strategy.select(population, fitness_scores_normalized)
        crossed_chromosomes = crossover_strategy.crossover(selected_chromosomes, params['crossover_probability'])
        mutated_chromosomes = mutation_strategy.mutate(crossed_chromosomes, params['mutation_probability'])

        if previous_max_chromosome == max_chromosome:
            generations_no_improve += 1
        else:
            generations_no_improve = 0


        previous_max_chromosome = max_chromosome
        population = mutated_chromosomes

        try:
            if params['time_limit'] < (time.time() - start):
                break
            if params['max_generations_no_improve'] < generations_no_improve:
                break
        except KeyError:
            pass

    end = time.time() - start
    return dict(
        time=end,
        epoch=epoch,
        average_fitness=average_fitness,
        max_fitness=max_fitness,
        max_solution=max_chromosome
    )


def assignement_problem_faq(distance_matrix, flow_matrix):
    start = time.time()
    res = quadratic_assignment(distance_matrix, flow_matrix, method='faq', options={'P0': 'randomized'})
    end = time.time() - start
    fitness_scores = compute_fitness_scores(list(res.col_ind + 1), distance_matrix, flow_matrix)

    max_fitness = np.min(fitness_scores)
    # min_fitness = np.max(fitness_scores)
    average_fitness = np.mean(fitness_scores)

    return dict(
        time=end,
        average_fitness=average_fitness,
        max_fitness=max_fitness,
        max_solution=res.col_ind + 1
    )


def assignement_problem_2opt(distance_matrix, flow_matrix):
    start = time.time()
    res = quadratic_assignment(distance_matrix, flow_matrix, method='2opt')
    end = time.time() - start
    fitness_scores = compute_fitness_scores(list(res.col_ind + 1), distance_matrix, flow_matrix)

    max_fitness = np.min(fitness_scores)
    # min_fitness = np.max(fitness_scores)
    average_fitness = np.mean(fitness_scores)

    return dict(
        time=end,
        average_fitness=average_fitness,
        max_fitness=max_fitness,
        max_solution=res.col_ind + 1
    )