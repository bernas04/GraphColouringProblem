import pygad
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

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

"""NUM_VERTICES = 50
NUM_EDGES = 1225"""

# PyGAD parameters
NUM_GENERATIONS = 2000
NUM_PARENTS_MATING = 50
NUM_SOLUTIONS_PER_POPULATION = 100


saturation = str(int(NUM_GENERATIONS * 0.1))  # 20% of the generations
# TODO: the reach_1 stop criteria is not well defined
# When the fitness function returns 1, it means that a solution with no conflicts was found
# but in our problem we want to find the BEST solution and not just a solution with no conflicts
STOP_CRITERIA = ["reach_1", "saturate_" + saturation]

"""
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
        adj_matrix[vertex2, vertex1] = 1"""

# Number of colors available
num_colors = len(adj_matrix)


def is_complete_graph(adj_matrix):
    num_vertices = len(adj_matrix)
    for i in range(num_vertices):
        for j in range(num_vertices):
            if i != j:
                if adj_matrix[i][j] != 1:
                    return False
            else:
                if adj_matrix[i][j] != 0:
                    return False
    return True


def has_cycles_and_odd_vertices(adj_matrix):
    num_vertices = len(adj_matrix)
    visited = [False] * num_vertices

    for vertex in range(num_vertices):
        if not visited[vertex]:
            if dfs_cycle(vertex, visited, -1, adj_matrix):
                return True

    return False


def dfs_cycle(vertex, visited, parent, adj_matrix):
    visited[vertex] = True

    for neighbor in range(len(adj_matrix[vertex])):
        if adj_matrix[vertex][neighbor]:
            if not visited[neighbor]:
                if dfs_cycle(neighbor, visited, vertex, adj_matrix):
                    return True
            elif neighbor != parent:
                return True

    return False


def is_star_shaped_graph(adj_matrix):
    num_vertices = len(adj_matrix)
    central_vertex_degree = 0
    vertex_degrees = [0] * num_vertices

    for i in range(num_vertices):
        for j in range(num_vertices):
            if adj_matrix[i][j] == 1:
                vertex_degrees[i] += 1
                if i != j:
                    vertex_degrees[j] += 1

    for degree in vertex_degrees:
        if degree == num_vertices - 1:
            central_vertex_degree += 1
        elif degree != 1:
            return False

    return central_vertex_degree == 1


def fitness_func(solution, solution_idx):
    """Calculate the fitness of the solution."""
    solution_num_colors = len(set(solution))
    conflicts = 0
    for i in range(len(adj_matrix)):
        for j in range(i + 1, len(adj_matrix)):
            if adj_matrix[i][j] and solution[i] == solution[j]:
                conflicts += 1

    difference = 0
    if is_complete_graph(adj_matrix) or has_cycles_and_odd_vertices(adj_matrix):
        chromaticNumber = sum(adj_matrix[0]) + 1
        difference = abs(chromaticNumber - solution_num_colors)

    elif is_star_shaped_graph(adj_matrix):
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
    """Check if the population has converged and print the fitness of the best solution in each generation"""
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

    # Show the image
    plt.show()


def run_ga():
    """Run the genetic algorithm to find a solution."""
    ga_instance = pygad.GA(
        num_generations=NUM_GENERATIONS,
        num_parents_mating=NUM_PARENTS_MATING,  # Number of solutions to be selected as parents
        fitness_func=fitness_func,
        sol_per_pop=NUM_SOLUTIONS_PER_POPULATION,  # population size
        # Number of genes in the solution/chromosome
        num_genes=len(adj_matrix),
        gene_type=int,
        gene_space=list(range(num_colors)),
        on_generation=on_generation,
        stop_criteria=STOP_CRITERIA,
    )

    ga_instance.run()
    ga_instance.summary()

    ga_instance.plot_fitness()

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
    run_ga()
