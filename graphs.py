import random
import math

def graph_generator(n, p):  # n = number of vertex, p = percentage of edges
    edges = []
    vertex = []

    #N must be between 0 and the length of our list of possible vertex
    for i in range(n):  # Generate vertex
        coordinates = []
        x = random.randint(1, 20)
        y = random.randint(1, 20)
        if ((x, y) in coordinates) == False:
            coordinates.append((x, y))
        # example: [ ['1', (3,2)], ['2', (1,5)], ...]
        vertex.append([i, (x, y)])

    min_edges = n-1
    max_edges = int(n*(n-1)/2)

    if n > 2:
        num_edges = int(p/100 * max_edges)
        print()
    else:
        num_edges = 1

    vertex_with_edges = set()

    # Build edges

    if min_edges <= num_edges <= max_edges:
        for i in range(num_edges):
            while True:
                v1 = random.choice(vertex)[0]
                v2 = random.choice(vertex)[0]
                if v1 != v2:
                    if (v1, v2) not in edges and (v2, v1) not in edges:
                        edges.append((v1, v2))
                        break
                    if len(vertex) != len(vertex_with_edges):  # conex graph
                        if v1 not in vertex_with_edges or v2 not in vertex_with_edges:
                            vertex_with_edges.update({v1, v2})
                            if ((v1, v2) in edges == False) and ((v2, v1) in edges) == False:
                                edges.append((v1, v2))
                            break

    print("Number of edges", len(edges))
    print("Number of vertex", len(vertex))

    return vertex, edges




def adjacency_matrix(edges):
    # Get the list of vertex
    vertex = set()
    num_edges = len(edges)

    for v1, v2 in edges:
        vertex.add(v1)
        vertex.add(v2)
    vertex = sorted(list(vertex))

    # Create an empty adjacency matrix
    num_vertex = len(vertex)
    adjacency_mtx = [[0] * num_vertex for _ in range(num_vertex)]

    # Fill the adjacency matrix based on the edges
    for v1, v2 in edges:
        i = vertex.index(v1)
        j = vertex.index(v2)
        adjacency_mtx[i][j] = 1
        adjacency_mtx[j][i] = 1
    #save the adjacency matrix in a file
    with open("adjacency_matrix_" + str(num_vertex) + "v_"+str(num_edges)+"e.txt", "w") as f:
        f.write("[")
        for row in adjacency_mtx:
            f.write(str(row) + ",")
            f.write("\n")
        f.write("]")

    return adjacency_mtx

def main():
    #16 vertex
    small_12 = {"vertices": [["A", [19, 8]], ["B", [9, 5]], ["C", [6, 16]], ["D", [2, 14]], ["E", [5, 19]], ["F", [3, 8]], ["G", [13, 8]], ["H", [2, 4]], ["I", [8, 7]], ["J", [16, 8]], ["K", [14, 2]], ["L", [14, 15]], ["M", [19, 14]], ["N", [14, 14]], ["O", [17, 17]], ["P", [14, 1]]], "edges": [["D", "O"], ["I", "O"], ["D", "K"], ["M", "G"], ["M", "O"], ["P", "K"], ["B", "J"], ["M", "I"], ["H", "A"], ["O", "E"], ["P", "E"], ["N", "L"], ["N", "F"], ["I", "B"]]}
    small_75 = {"vertices": [["A", [2, 5]], ["B", [2, 3]], ["C", [20, 20]], ["D", [1, 20]], ["E", [2, 14]], ["F", [7, 16]], ["G", [17, 16]], ["H", [8, 7]], ["I", [5, 1]], ["J", [6, 19]], ["K", [16, 11]], ["L", [13, 5]], ["M", [13, 2]], ["N", [11, 12]], ["O", [11, 12]], ["P", [7, 18]]], "edges": [["F", "H"], ["I", "D"], ["B", "N"], ["D", "K"], ["O", "A"], ["P", "H"], ["B", "J"], ["G", "N"], ["H", "A"], ["E", "C"], ["J", "K"], ["B", "A"], ["K", "L"], ["D", "M"], ["J", "P"], ["E", "J"], ["P", "M"], ["N", "C"], ["F", "L"], ["H", "B"], ["D", "E"], ["I", "N"], ["F", "A"], ["I", "G"], ["E", "K"], ["P", "L"], ["K", "G"], ["E", "O"], ["A", "P"], ["M", "E"], ["F", "J"], ["P", "B"], ["L", "E"], ["J", "H"], ["C", "B"], ["N", "A"], ["A", "K"], ["N", "H"], ["P", "G"], ["O", "G"], ["B", "I"], ["E", "I"], ["C", "P"], ["M", "H"], ["G", "A"], ["A", "J"], ["M", "F"], ["B", "K"], ["F", "I"], ["G", "H"], ["J", "N"], ["N", "E"], ["C", "O"], ["C", "K"], ["D", "J"], ["N", "M"], ["H", "L"], ["B", "D"], ["H", "O"], ["H", "E"], ["G", "L"], ["I", "M"], ["M", "G"], ["G", "C"], ["C", "I"], ["C", "A"], ["C", "J"], ["O", "F"], ["K", "I"], ["B", "F"], ["G", "F"], ["F", "P"], ["H", "K"], ["D", "F"], ["A", "M"], ["B", "M"], ["A", "D"], ["B", "L"], ["J", "L"]]}
    adjacency_matrix(small_12["edges"])
    adjacency_matrix(small_75["edges"])

    #50 vertex
    medium_12 = graph_generator(50,12.5)
    medium_75 = graph_generator(50,75)


    #1000 vertex
    big_12 = graph_generator(1000,12.5)
    big_75 = graph_generator(1000,75)

    
    adjacency_matrix(medium_12[1])
    adjacency_matrix(medium_75[1])
    adjacency_matrix(big_12[1])
    adjacency_matrix(big_75[1])
    
    
    # save the adjacency matrix in a file

    

    """
    print("Adjacency matrix of medium graph with 12.5 of edges")
    for row in adjacency_matrix_medium_12:
        print(row)
    
    print("Adjacency matrix of medium graph with 75 of edges")
    for row in adjacency_matrix_medium_75:
        print(row)
    """



main()