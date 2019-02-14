import networkx as nx
import os
import k_means_clustering as ss
from output_scorer import score_output


###########################################
# Change this variable to the path to
# the folder containing all three input
# size category folders
###########################################
path_to_inputs = "./all_inputs"

###########################################
# Change this variable if you want
# your outputs to be put in a
# different folder
###########################################
path_to_outputs = "./outputs"

def parse_input(folder_name):
    '''
        Parses an input and returns the corresponding graph and parameters

        Inputs:
            folder_name - a string representing the path to the input folder

        Outputs:
            (graph, num_buses, size_bus, constraints)
            graph - the graph as a NetworkX object
            num_buses - an integer representing the number of buses you can allocate to
            size_buses - an integer representing the number of students that can fit on a bus
            constraints - a list where each element is a list vertices which represents a single rowdy group
    '''
    graph = nx.read_gml(folder_name + "/graph.gml")
    parameters = open(folder_name + "/parameters.txt")
    num_buses = int(parameters.readline())
    size_bus = int(parameters.readline())
    constraints = []

    for line in parameters:
        line = line[1: -2]
        curr_constraint = [num.replace("'", "") for num in line.split(", ")]
        constraints.append(curr_constraint)

    return graph, num_buses, size_bus, constraints

def solve(size, graph, num_buses, size_bus, constraints):
    #TODO: Write this method as you like. We'd recommend changing the arguments here as well
    '''
    size = medium, small, or large
    graph = networkx graph
    num_buses = number of buses we need to form
    size_bus = maximum capacity of each bus
    constraints = the list of lists for the rowdy groups
    '''
    if size == "small":
        solution = ss.solver(graph, num_buses, size_bus, constraints)
        return solution
    elif size == "medium":
        solution = ss.solver(graph, num_buses, size_bus, constraints)
        return solution
    else:
        solution = ss.solver(graph, num_buses, size_bus, constraints)
        return solution


def main():
    '''
        Main method which iterates over all inputs and calls `solve` on each.
        The student should modify `solve` to return their solution and modify
        the portion which writes it to a file to make sure their output is
        formatted correctly.
    '''
    size_categories = ["small", "medium", "large"]
    final_score = 0
    num_processed = 0
    if not os.path.isdir(path_to_outputs):
        os.mkdir(path_to_outputs)

    for size in size_categories:
        category_path = path_to_inputs + "/" + size
        output_category_path = path_to_outputs + "/" + size
        category_dir = os.fsencode(category_path)

        if not os.path.isdir(output_category_path):
            os.mkdir(output_category_path)

        for input_folder in os.listdir(category_dir):
            input_name = os.fsdecode(input_folder)
            graph, num_buses, size_bus, constraints = parse_input(category_path + "/" + input_name)
            output_file = open(output_category_path + "/" + input_name + ".out", "w")
            print("Running solver with {0} and {1}".format(category_path + "/" + input_name, output_category_path + "/" + input_name + ".out"))
            solution = solve(size, graph, num_buses, size_bus, constraints)
            for final_cluster in solution:
                output_file.write(str(final_cluster) + "\n")
            print("\n")
            output_file.close()
            score, msg = score_output(category_path + "/" + input_name, output_category_path + "/" + input_name + ".out")
            final_score += score
            num_processed += 1
            print("Got score {0}".format(score))

        print("Final average score: " + str(final_score/num_processed))

if __name__ == '__main__':
    main()
