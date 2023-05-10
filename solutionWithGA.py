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

adj_matrix = np.zeros((25, 25))

# randomly assign 290 edges in the graph
for i in range(290):
    # randomly select two vertices
    vertex1 = np.random.randint(0, 25)
    vertex2 = np.random.randint(0, 25)
    
    # make sure the vertices are not the same and there is no edge already
    if vertex1 != vertex2 and adj_matrix[vertex1, vertex2] == 0:
        # set the edge
        adj_matrix[vertex1, vertex2] = 1
        adj_matrix[vertex2, vertex1] = 1

# Number of colors available
num_colors = 10 # number of vertex

def fitness_func(solution, solution_idx):
    """Calculate the fitness of the solution."""
    conflicts = 0
    for i in range(len(adj_matrix)):
        for j in range(i+1, len(adj_matrix)):
            if adj_matrix[i][j] and solution[i] == solution[j]:
                conflicts += 1
    # return a fitness that minimizes the number of conflicts
    return 1 / (conflicts + 1) # formula with max number of colors and minimum 

def on_generation(ga_instance):
    """Print the fitness of the best solution in each generation."""
    print(f'Generation {ga_instance.generations_completed}: Best fitness = {ga_instance.best_solution()}')

def run_ga():
    """Run the genetic algorithm to find a solution."""
    ga_instance = pygad.GA(num_generations=20000, 
                           num_parents_mating=50, #Number of solutions to be selected as parents
                           fitness_func=fitness_func,
                           sol_per_pop=100, #population size
                           num_genes=len(adj_matrix), #: Number of genes in the solution/chromosome
                           gene_type=int,
                           gene_space=list(range(num_colors)),
                           on_generation=on_generation)
    ga_instance.run()

    # Print the best solution
    print('Best solution:', ga_instance.best_solution()[0])

if __name__ == '__main__':
    run_ga()
