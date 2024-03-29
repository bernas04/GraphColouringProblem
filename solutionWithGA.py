import pygad
import time
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import warnings
import os
warnings.filterwarnings("ignore")

# Verifies if the graph is complete 
def is_complete_graph():
    for i in range(num_vertices_and_colors):
        for j in range(num_vertices_and_colors):
            if i != j:
                if adj_matrix[i][j] != 1:
                    return False
            else:
                if adj_matrix[i][j] != 0:
                    return False
    return True

# Verifies if the graph has cycles and odd vertices
def has_cycles_and_odd_vertices():
    visited = [False] * num_vertices_and_colors

    for vertex in range(num_vertices_and_colors):
        if not visited[vertex]:
            if dfs_cycle(vertex, visited, -1):
                return True

    return False

# Verify if the graph has cycles
def dfs_cycle(vertex, visited, parent):
    visited[vertex] = True

    for neighbor in range(len(adj_matrix[vertex])):
        if adj_matrix[vertex][neighbor]:
            if not visited[neighbor]:
                if dfs_cycle(neighbor, visited, vertex):
                    return True
            elif neighbor != parent:
                return True

    return False

# Verifies if the graph is star shaped
def is_star_shaped_graph():
    central_vertex_degree = 0
    vertex_degrees = [0] * num_vertices_and_colors

    for i in range(num_vertices_and_colors):
        for j in range(num_vertices_and_colors):
            if adj_matrix[i][j] == 1:
                vertex_degrees[i] += 1
                if i != j:
                    vertex_degrees[j] += 1

    for degree in vertex_degrees:
        if degree == num_vertices_and_colors - 1:
            central_vertex_degree += 1
        elif degree != 1:
            return False

    return central_vertex_degree == 1

def fitness_func(solution, solution_idx):
    """Calculate the fitness of the solution."""
    conflicts = 0
    for i in range(num_vertices_and_colors):
        for j in range(i + 1, num_vertices_and_colors):
            if adj_matrix[i][j] and solution[i] == solution[j]:
                conflicts += 1

    solution_num_colors = len(set(solution))
    difference = 0
    if is_complete_graph() or has_cycles_and_odd_vertices():
        chromaticNumber = sum(adj_matrix[0]) + 1
        difference = abs(chromaticNumber - solution_num_colors)
    elif is_star_shaped_graph():
        chromaticNumber = 2
        difference = abs(chromaticNumber - solution_num_colors)

    # return a fitness that minimizes the number of conflicts, and the difference between the number of colors used and the chromatic number of the graph
    return 1 / (conflicts + difference + 1)

def on_generation(ga_instance):
    """Print the fitness of the best solution in each generation"""
    #print(f"Generation {ga_instance.generations_completed}: Best fitness = {ga_instance.best_solution()}")


def convert_to_graph_image(color_list, fileDir):
    G = nx.from_numpy_array(adj_matrix)

    # Set node colors
    nodes = G.nodes()
    node_colors = [color_list[node] for node in nodes]

    # Set node positions
    pos = nx.spring_layout(G)

    # Draw the graph
    nx.draw_networkx_nodes(
        G, pos, node_color=node_colors, cmap="coolwarm", node_size=500
    )
    nx.draw_networkx_edges(G, pos, edge_color="gray")
    nx.draw_networkx_labels(G, pos)

    # Remove axis labels
    plt.axis("off")

    # Save the image
    plt.savefig(fileDir)
    plt.close()


def run_ga():
    """Run the genetic algorithm to find a solution."""
    ga_instance = pygad.GA(
        num_generations=num_generations,
        num_parents_mating=num_parents_mating,  # Number of solutions to be selected as parents
        fitness_func=fitness_func,
        sol_per_pop=num_solutions_per_population,  # population size
        num_genes=num_vertices_and_colors, # Number of genes in the solution/chromosome
        gene_type=int,
        gene_space=list(range(num_vertices_and_colors)),
        on_generation=on_generation,
        stop_criteria=STOP_CRITERIA,
        crossover_probability=crossover_probability,
        mutation_probability=mutation_probability,
    )

    execution_time = time.time()
    ga_instance.run()
    execution_time = time.time() - execution_time
    #ga_instance.summary()

    return ga_instance, execution_time 

if __name__ == "__main__":

    # Adjacency matrix representing the graph
    adj_matrix = np.array(
[[0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
[0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1],
[1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1],
[1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
[0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
[1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0],
[1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1],
[1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
[1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0],
[1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1],
[1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0],
[0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0]]
    )

    best_solution_at_the_moment = None
    best_execution_time = 0
    best_parameters = {}

    num_edges = sum(sum([i for i in adj_matrix]))
    num_vertices_and_colors = len(adj_matrix) # Number of colors available, and number of vertices in the graph

    num_generations_list = [100, 500, 1000, 2000]
    num_parents_mating_list = [10, 20, 30, 40, 50]
    num_solutions_per_population_list = [20, 40, 60, 80, 100]
    crossover_probabilities = [0.5, 0.7, 0.9] 
    mutation_probabilities = [0.01, 0.05, 0.1]  
    for num_generations in num_generations_list:
        saturation = str(int(num_generations * 0.1)) 
        STOP_CRITERIA = ["reach_1", "saturate_" + saturation]
        for num_parents_mating in num_parents_mating_list:
            for num_solutions_per_population in num_solutions_per_population_list:
                for crossover_probability in crossover_probabilities:
                    for mutation_probability in mutation_probabilities:
                        if num_solutions_per_population > num_parents_mating:
                            print("Number of generations: %d ; Number of parents mating: %d ; Number of solutions per population: %d ; Crossover probability: %f ; Mutation probability: %f" % (num_generations, num_parents_mating, num_solutions_per_population, crossover_probability, mutation_probability))
                            ga_instance, executionTime = run_ga()
                            # Print the best solution with these parameters
                            print("Best solution with these parameters:", ga_instance.best_solution()[0],", score", ga_instance.best_solution()[1])
                            if best_solution_at_the_moment == None or ga_instance.best_solution()[1] > best_solution_at_the_moment.best_solution()[1]:
                                
                                best_solution_at_the_moment = ga_instance
                                best_execution_time = executionTime
                                best_parameters["num_generations"] = num_generations
                                best_parameters["num_parents_mating"] = num_parents_mating
                                best_parameters["num_solutions_per_population"] = num_solutions_per_population
                                best_parameters["crossover_probability"] = crossover_probability
                                best_parameters["mutation_probability"] = mutation_probability
                            print("--------------------------------------------------")
                            print()

    directory_name = f"results/{num_vertices_and_colors}v{num_edges}e"
    if not os.path.isdir(directory_name):
        os.mkdir(directory_name)

    f = open(f"{directory_name}/solution.txt", "w")
    f.write(f"n_vertex: {num_vertices_and_colors}\n")
    f.write(f"n_edges: {num_edges}\n")
    f.write(f"best_parameters: {best_parameters}\n")
    f.write(f"execution_time: {best_execution_time}\n")
    f.write(f"accuracy: {best_solution_at_the_moment.best_solution()[1]}\n")
    f.close()

    convert_to_graph_image(best_solution_at_the_moment.best_solution()[0], f"{directory_name}/coloredGraph.png")

    best_solution_at_the_moment.plot_fitness(
        save_dir=f"{directory_name}/generationsFitness.png"
        )
