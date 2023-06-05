import pygad
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import warnings
warnings.filterwarnings("ignore")

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

def has_cycles_and_odd_vertices():
    visited = [False] * num_vertices_and_colors

    for vertex in range(num_vertices_and_colors):
        if not visited[vertex]:
            if dfs_cycle(vertex, visited, -1):
                return True

    return False

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

    return 1 / (conflicts + difference + 1)

    """else:
        chromaticNumber = 0
        for i in adj_matrix:
            chromaticNumber = (
                sum(adj_matrix[i])
                if sum(adj_matrix[i]) > chromaticNumber
                else chromaticNumber
            )

    # return a fitness that minimizes the number of conflicts
    return 1 / (conflicts + 1)"""


def on_generation(ga_instance):
    """Print the fitness of the best solution in each generation"""
    print(
        f"Generation {ga_instance.generations_completed}: Best fitness = {ga_instance.best_solution()}"
    )


def convert_to_graph_image(color_list):
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
    plt.savefig(f"results/graph_6vertices/solution_num_generations_{num_generations}_num_parents_mating_{num_parents_mating}_num_solutions_per_population_{num_solutions_per_population}_crossover_probability_{crossover_probability}_mutation_probability_{mutation_probability}.png")
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

    ga_instance.run()
    ga_instance.summary()
    ga_instance.plot_fitness(save_dir=f"results/graph_6vertices/generations_vs_fitness_num_generations_{num_generations}_num_parents_mating_{num_parents_mating}_num_solutions_per_population_{num_solutions_per_population}_crossover_probability_{crossover_probability}_mutation_probability_{mutation_probability}.png")
    plt.close()

    # Print the best solution
    print(
        "Best solution:",
        ga_instance.best_solution()[0],
        ", score",
        ga_instance.best_solution()[1],
    )

    # Convert the best solution to a graph image
    convert_to_graph_image(ga_instance.best_solution()[0])


if __name__ == "__main__":

    # Adjacency matrix representing the graph
    adj_matrix = np.array(
        [
            [0, 1, 1, 0, 0, 0],
            [1, 0, 1, 1, 0, 0],
            [1, 1, 0, 1, 1, 0],
            [0, 1, 1, 0, 1, 1],
            [0, 0, 1, 1, 0, 1],
            [0, 0, 0, 1, 1, 0],
        ]
    )
    num_vertices_and_colors = len(adj_matrix) # Number of colors available, and number of vertices in the graph
    num_generations_list = [100, 200, 300]
    num_parents_mating_list = [10, 20, 30]
    num_solutions_per_population_list = [20, 30, 40]
    crossover_probabilities = [0.5, 0.7, 0.9]
    mutation_probabilities = [0.01, 0.05, 0.1]
    for num_generations in num_generations_list:
        saturation = str(int(num_generations * 0.1)) #mudar saturation? como nos parametros
        STOP_CRITERIA = ["reach_1", "saturate_" + saturation]
        for num_parents_mating in num_parents_mating_list:
            for num_solutions_per_population in num_solutions_per_population_list:
                for crossover_probability in crossover_probabilities:
                    for mutation_probability in mutation_probabilities:
                        if num_solutions_per_population > num_parents_mating:
                            print("Number of generations: %d ; Number of parents mating: %d ; Number of solutions per population: %d ; Crossover probability: %f ; Mutation probability: %f" % (num_generations, num_parents_mating, num_solutions_per_population, crossover_probability, mutation_probability))
                            run_ga()
                            print("--------------------------------------------------")
                            print()