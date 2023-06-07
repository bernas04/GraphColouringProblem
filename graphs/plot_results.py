import os 
import matplotlib.pyplot as plt
import numpy as np


def plot_results_vertex_():
    directory_path = 'results/'
    data = []

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        open_file = open(file_path, "r")

        lines = open_file.readlines()
        n_vertex = 0
        time = 0

        for line in lines:
            if line.startswith('n_vertex'):
                n_vertex = int(line.split(':')[1])
        
            elif line.startswith('execution_time'):
                time = float(line.split(':')[1])
            
        data.append([n_vertex, time, filename])
  
    # Plotting the results
    for data_point in data:
        vertex, time, filename = data_point
        plt.scatter(vertex, time, label=filename)

    plt.xlabel('Number of Vertices')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Vertex vs Execution Time')
    plt.legend()
    plt.show()

plot_results_vertex_() 

