import pygad
import numpy as np

# Adjacency matrix representing the graph
""" adj_matrix = np.array([
    [0, 1, 1, 0, 0, 0],
    [1, 0, 1, 1, 0, 0],
    [1, 1, 0, 1, 1, 0],
    [0, 1, 1, 0, 1, 1],
    [0, 0, 1, 1, 0, 1],
    [0, 0, 0, 1, 1, 0]
]) """

NUM_VERTICES = 50
NUM_EDGES = 1225

adj_matrix = np.zeros((NUM_VERTICES, NUM_VERTICES))

# randomly assign NUM_EDGES edges in the graph
for i in range(NUM_EDGES):
    # randomly select two vertices
    vertex1 = np.random.randint(0, NUM_VERTICES)
    vertex2 = np.random.randint(0, NUM_VERTICES)

    # make sure the vertices are not the same and there is no edge already
    if vertex1 != vertex2 and adj_matrix[vertex1, vertex2] == 0:
        # set the edge
        adj_matrix[vertex1, vertex2] = 1
        adj_matrix[vertex2, vertex1] = 1

# Number of colors available
num_colors = NUM_VERTICES

def fitness_func(solution, solution_idx):
    """Calculate the fitness of the solution."""
    conflicts = 0
    for i in range(len(adj_matrix)):
        for j in range(i+1, len(adj_matrix)):
            if adj_matrix[i][j] and solution[i] == solution[j]:
                conflicts += 1
    # return a fitness that minimizes the number of conflicts
    return 1 / (conflicts + 1)


def on_generation(ga_instance):
    """Check if the population has converged and print the fitness of the best solution in each generation"""
    print(f'Generation {ga_instance.generations_completed}: Best fitness = {ga_instance.best_solution()}')

    n = 10  # number of generations to check
    best_fitness = ga_instance.best_solution()[1]
    last_n_fitness = [s[1] for s in ga_instance.best_solutions[-n:]]
    print(last_n_fitness)
    if all(abs(f - best_fitness) < 0.0001 for f in last_n_fitness):
        print(f"Population has converged. Best fitness value has not changed significantly over the last {n} generations.")
        return "stop"

    return "stop" if ga_instance.best_solution()[1] == 1 else False

def run_ga():
    """Run the genetic algorithm to find a solution."""
    ga_instance = pygad.GA(num_generations=2000,
                           num_parents_mating=50,  # Number of solutions to be selected as parents
                           fitness_func=fitness_func,
                           sol_per_pop=100,  # population size
                           num_genes=len(adj_matrix), # Number of genes in the solution/chromosome
                           gene_type=int,
                           gene_space=list(range(num_colors)),
                           on_generation=on_generation,
                           save_best_solutions=True)

    ga_instance.run()

    # Print the best solution
    print('Best solution:', ga_instance.best_solution()[0], ", score", ga_instance.best_solution()[1])


if __name__ == '__main__':
    run_ga()
