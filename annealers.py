from simanneal import Annealer
import random

class SchoolBusProblem(Annealer):
    
    """Test annealer for the school bus problem as described in the spec."""
    
    """ The annealer makes use of a self.state variable.
        In the context of this project, the self.state should be a tuple.
        First element of tuple: dictionary mapping clusters to their subgraphs.
        Second element of tuple: the constraints
        Third element is the graph
        """
    
    def move(self):
        """Swaps two nodes that are in separate clusters."""
        
        clusters = self.state[0]
        constraints = self.state[1]
        graph = self.state[2]
        size_bus = self.state[3]
        
        probability = random.random()
        
        # pick two random clusters
        a_cluster = random.randint(0, len(clusters.keys()) - 1)
        b_cluster = random.randint(0, len(clusters.keys()) - 1)
        
        valid =  (len(clusters[a_cluster]) >  1) and (len(clusters[b_cluster]) < size_bus)
        move_made = False
        node = None
        
        if (probability > 0.5) and valid:
            #move
            # pick two random nodes to swap from those clusters
            
            for constraint in constraints:
                if set(constraint) < set(clusters[a_cluster]):
                    node = random.choice(constraint)
                    break
        
            if node:
                
                a_index = clusters[a_cluster].index(node)
                a_node = clusters[a_cluster].pop(a_index)
                clusters[b_cluster].append(a_node)
                
                self.state = [clusters, constraints, graph, size_bus]
                move_made = True
    
    if move_made == False:
        
        #print("Performing swap between clusters {0} and {1}".format(a_cluster, b_cluster))
        
        # pick two random nodes to swap from those clusters
        a_index = random.randint(0, len(clusters[a_cluster]) - 1)
        b_index = random.randint(0, len(clusters[b_cluster]) - 1)
        
        #print("Performing swap between indexes {0} and {1}".format(a_index, b_index))
        
        # perform the swap
        #print("Swapping nodes {0} and {1}".format(clusters[a_cluster][a_index], clusters[b_cluster][b_index]))
        clusters[a_cluster][a_index], clusters[b_cluster][b_index] = clusters[b_cluster][b_index], clusters[a_cluster][a_index]
            
            # change the state to reflect the changes
            self.state = [clusters, constraints, graph, size_bus]

def energy(self):
    """Calculates the number of rowdy groups violated."""
        
        clusters = self.state[0]
        constraints = self.state[1]
        graph = self.state[2]
        
        score = score_output(clusters, constraints, graph.copy())
        #print('Current energy: ' + str(score))
        return score

def score_output(clusters, constraints, graph):
    
    # if len(clusters) != num_buses:
    #     return -1, "Must assign students to exactly {} buses, found {} buses".format(num_buses, len(assignments))
    #
    # # make sure no bus is empty or above capacity
    # for i in range(len(assignments)):
    #     if len(assignments[i]) > size_bus:
    #         return -1, "Bus {} is above capacity".format(i)
    #     if len(assignments[i]) <= 0:
    #         return -1, "Bus {} is empty".format(i)
    
    assignments = clusters
    bus_assignments = {}
    attendance_count = 0
    
    # make sure each student is in exactly one bus
    attendance = {student:False for student in graph.nodes()}
    
    for i in range(len(assignments)):
        
        if not all([student in graph for student in assignments[i]]):
            return -1, "Bus {} references a non-existant student: {} from this graph: {}".format(i, assignments[i], list(graph.nodes()))
    
        for student in assignments[i]:
            # if a student appears more than once
            if attendance[student] == True:
                print(assignments[i])
                return -1, "{0} appears more than once in the bus assignments".format(student)
            
            attendance[student] = True
            bus_assignments[student] = i

# make sure each student is accounted for
if not all(attendance.values()):
    return -1, "Not all students have been assigned a bus"
    
    total_edges = graph.number_of_edges()
    
    # Remove nodes for rowdy groups which were not broken up
    for i in range(len(constraints)):
        busses = set()
        for student in constraints[i]:
            busses.add(bus_assignments[student])
        if len(busses) <= 1:
            for student in constraints[i]:
                if student in graph:
                    graph.remove_node(student)

# score output
score = 0
    for edge in graph.edges():
        if bus_assignments[edge[0]] == bus_assignments[edge[1]]:
            score += 1
score = score / total_edges
    return -score
