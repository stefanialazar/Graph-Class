import copy
import random
import sys
from collections import deque


# function to remove a node from a graph
def remove_node(this_graph, delete_value):
    if delete_value in this_graph:
        del this_graph[delete_value]
    for edges in this_graph.values():
        copy_edge = copy.deepcopy(edges)
        if delete_value in copy_edge:
            edges.remove(delete_value)


# deep first search for a graph
def dfs(this_graph, starting_node):
    stack, result = [starting_node], []
    while stack:
        node = stack.pop()
        if node in result:
            continue
        result.append(node)
        if node in this_graph:
            for node1 in this_graph[node]:
                stack.append(node1)
    return result


# find the number of connected components
def dfs_connected(this_graph):
    visit = []
    connected = 0
    components = []
    for nod in range(1, N + 1):
        if nod not in visit:
            connected += 1
            result_dfs = dfs(this_graph, nod)
            components.append(result_dfs)
            for each_node in result_dfs:
                visit.append(each_node)
    return components


class Graph:

    # initialize the graph
    def __init__(self, nr_nodes):
        # dictionary to store graph
        self.graph = {}

        # list of nodes
        self.my_nodes = [x for x in range(1, nr_nodes + 1)]

        # No. of nodes
        self.nr_of_nodes = nr_nodes

    # function to add an edge to graph
    def add_edge(self, node1, node2):
        temp = []
        if node1 not in self.graph:
            temp.append(node2)
            self.graph[node1] = temp
        elif node1 in self.graph:
            temp.extend(self.graph[node1])
            temp.append(node2)
            self.graph[node1] = temp

    # function to add a weighted edge to graph
    def add_weighted_edge(self, node1, node2, weight):
        temp = []
        if node1 not in self.graph:
            temp.append((node2, weight))
            self.graph[node1] = temp
        elif node1 in self.graph:
            temp.extend(self.graph[node1])
            temp.append((node2, weight))
            self.graph[node1] = temp

    # read the unweighted, undirected graph from input file
    def read_unweighted_undirected_graph(self, nr_edges):
        for i in range(nr_edges):
            x, y = [int(z) for z in f.readline().split()]
            self.add_edge(x, y)
            self.add_edge(y, x)

    # read the unweighted, directed graph from input file
    def read_unweighted_directed_graph(self, nr_edges):
        for i in range(nr_edges):
            x, y = [int(z) for z in f.readline().split()]
            self.add_edge(x, y)

    # read the weighted, undirected graph from input file
    def read_weighted_undirected_graph(self, nr_edges):
        for i in range(nr_edges):
            x, y, w = [int(z) for z in f.readline().split()]
            self.add_weighted_edge(x, y, w)
            self.add_weighted_edge(y, x, w)

    # read the weighted, directed graph from input file
    def read_weighted_directed_graph(self, nr_edges):
        for i in range(nr_edges):
            x, y, w = [int(z) for z in f.readline().split()]
            self.add_weighted_edge(x, y, w)

    # read the weighted, directed graph from input file
    def read_weighted_directed_graph_royfloyd(self, nr_edges):
        current_node = 1
        matrix = []
        for i in range(nr_edges):
            val = [int(z) for z in f.readline().split()]
            matrix.append(val)
            for j in range(len(val)):
                if val[j] != 0:
                    self.add_weighted_edge(current_node, j+1, val[j])
            current_node += 1
        return matrix

    # original dfs
    def dfs(self, starting_node):
        stack, result = [starting_node], []
        while stack:
            node = stack.pop()
            if node in result:
                continue
            result.append(node)
            if node in self.graph:
                for node1 in self.graph[node]:
                    stack.append(node1)
        return result

    # original bfs
    def bfs(self, starting_node):
        queue, result = deque(), [starting_node]
        queue.append(starting_node)
        while queue:
            node = queue.popleft()
            aux = []
            if node in self.graph:
                for n in self.graph[node]:
                    if n not in result:
                        queue.append(n)
                        aux.append(n)
            if aux:
                for each_node in aux:
                    result.append(each_node)
        return result

    # Part I : dfs
    # find the number of connected components for a graph in my class
    def dfs_connected(self):
        visit = []
        connected = 0
        components = []
        for nod in range(1, N + 1):
            if nod not in visit:
                connected += 1
                result_dfs = self.dfs(nod)
                components.append(result_dfs)
                for each_node in result_dfs:
                    visit.append(each_node)
        return components

    # Part I : bfs
    # get the shortest distance from starting node to each node in distance with breath first search
    def bfs_shortest(self, starting_node):
        distance = {}
        for node in self.my_nodes:
            distance[node] = -1
        distance[starting_node] = 0
        queue, result = deque(), [starting_node]
        queue.append(starting_node)
        while queue:
            node = queue.popleft()
            aux = []
            if node in self.graph:
                for n in self.graph[node]:
                    if n not in result:
                        queue.append(n)
                        aux.append(n)
                        distance[n] = distance[node] + 1
            if aux:
                for each_node in aux:
                    result.append(each_node)
        return distance

    # Part I : ctc
    # function to find strongly connected component in a directed graph
    def find_ctc_components(self):
        trans_graph = {}
        for node, edges in self.graph.items():
            for node2 in edges:
                temp = []
                if node2 not in trans_graph:
                    temp.append(node)
                    trans_graph[node2] = temp
                elif node2 in trans_graph:
                    temp.extend(trans_graph[node2])
                    temp.append(node)
                    trans_graph[node2] = temp
        ctc = []
        copy_graph = copy.deepcopy(self.graph)
        while self.graph:
            nod = random.choice(list(self.graph.keys()))
            result_dfs = dfs(self.graph, nod)
            trans_result_dfs = dfs(trans_graph, nod)
            plus_minus = list(set(result_dfs) & set(trans_result_dfs))
            ctc.append(plus_minus)
            for member in plus_minus:
                remove_node(self.graph, member)
                remove_node(trans_graph, member)
        # if keys are left in trans_adj_list then they are from ctc
        for nod in trans_graph.keys():
            aux = [nod]
            ctc.append(aux)
        self.graph = copy.deepcopy(copy_graph)
        return ctc

    # Part I : sortaret
    # function to find topological order in a directed acyclic graph
    def find_topological_order(self):
        incoming_degree = {}
        topological_queue = []
        topological_order = []
        for node in self.my_nodes:
            incoming_degree[node] = 0
        for edges in self.graph.values():
            for edge in edges:
                incoming_degree[edge] += 1
        copy_graph = copy.deepcopy(self.graph)
        while self.graph:
            for node, income in incoming_degree.items():
                if income == 0:
                    topological_queue.append(node)
                    incoming_degree[node] = -1
            while topological_queue:
                node_to_remove = topological_queue.pop(0)
                topological_order.append(node_to_remove)
                if node_to_remove in self.graph:
                    for edge in self.graph[node_to_remove]:
                        incoming_degree[edge] -= 1
                    remove_node(self.graph, node_to_remove)
        for node, income in incoming_degree.items():
            if income == 0:
                topological_order.append(node)
        self.graph = copy.deepcopy(copy_graph)
        return topological_order

    # Part I : Critical Connections in a Network
    # function to find critical connections in a  graph
    def find_articulation_edge(self):
        articulation_edge = []
        visited_edges = []
        new_graph = copy.deepcopy(self.graph)
        for node, edges in self.graph.items():
            for edge in edges:
                visit = []
                connected = 0
                if sorted([node, edge]) not in visited_edges:
                    self.graph[node].remove(edge)
                    self.graph[edge].remove(node)
                    visited_edges.append(sorted([node, edge]))
                    for nod in self.graph.keys():
                        if nod not in visit:
                            connected += 1
                            result_dfs = dfs(self.graph, nod)
                            for each_node in result_dfs:
                                visit.append(each_node)
                    if connected > 1:
                        articulation_edge.append([node, edge])
                    self.graph = copy.deepcopy(new_graph)
                else:
                    continue
        return articulation_edge

    # Part II : dijkstra
    # function to use Dijkstra's algorithm from node 1
    def dijkstra(self):
        unvisited = [x for x in self.my_nodes]
        distance = {1: 0}
        for x in self.my_nodes[1:]:
            distance[x] = sys.maxsize
        searched_node = 1
        while unvisited:
            min_dist = sys.maxsize
            for node, dist in distance.items():
                if dist <= min_dist and node in unvisited:
                    min_dist = dist
                    searched_node = node
            if searched_node in self.graph:
                for neighbour in self.graph[searched_node]:
                    if distance[searched_node] + neighbour[1] < distance[neighbour[0]]:
                        distance[neighbour[0]] = distance[searched_node] + neighbour[1]
            unvisited.remove(searched_node)
        return [x for x in distance.values()]

    # function to use Bellman-Ford algorithm
    # def bellman_ford(self):
    #     distance = {1: 0}
    #     for x in self.my_nodes[1:]:
    #         distance[x] = sys.maxsize
    #     for i in range(0, len(self.my_nodes)-1):
    #         for starting_node, ending_node in self.graph.items():
    #             if distance[starting_node] + ending_node[1]

    # Part II : apm
    # function to use Kruskal algorithm
    def kruskal(self):
        my_edges = []
        cost_min = 0
        tree_edges = []
        for node, edges in self.graph.items():
            for edge in edges:
                aux = [node]
                aux.extend(edge)
                my_edges.append(aux)
        my_edges.sort(key=lambda k: k[2])
        tree_edges.append([my_edges[0][0], my_edges[0][1]])
        cost_min += my_edges[0][2]
        for edge in my_edges[1:]:
            visit = []
            connected_components = []
            for each_edge in tree_edges:
                for nod in each_edge:
                    if nod not in visit:
                        stack, result = [nod], []

                        while stack:
                            node = stack.pop()
                            if node in result:
                                continue
                            result.append(node)
                            for each_edge1 in tree_edges:
                                if each_edge1[0] == node:
                                    stack.append(each_edge1[1])
                                elif each_edge1[1] == node:
                                    stack.append(each_edge1[0])

                        connected_components.append(result)
                        for each_node in result:
                            visit.append(each_node)
            already_in = 0
            for component in connected_components:
                if edge[0] in component and edge[1] in component:
                    already_in = 1
                    break
            if already_in == 0:
                tree_edges.append([edge[0], edge[1]])
                cost_min += edge[2]
        return cost_min, len(tree_edges), tree_edges

    # Part III : darb
    # length of the farthest distance from two nodes of a tree
    def diameter_tree(self):
        x = random.randint(1, self.nr_of_nodes)
        first_bfs = self.bfs(x)
        second_bfs = self.bfs(first_bfs[-1])
        current_node = second_bfs[0]
        next_index = 1
        distance = [current_node]
        while current_node != 1:
            if second_bfs[next_index] in self.graph[current_node]:
                distance.append(second_bfs[next_index])
                current_node = second_bfs[next_index]
                next_index += 1
            else:
                next_index += 1
        current_node = second_bfs[-1]
        next_index = len(second_bfs)-2
        distance2 = [current_node]
        while current_node != 1:
            if second_bfs[next_index] in self.graph[current_node]:
                distance2.append(second_bfs[next_index])
                current_node = second_bfs[next_index]
                next_index -= 1
            else:
                next_index -= 1
        distance.extend(reversed(distance2[:-1]))
        return distance

    # Part III : royfloyd
    # Floyd–Warshall/Roy-Floyd algorithm
    def royfloyd(self, matrix):
        for k in range(self.nr_of_nodes):
            for i in range(self.nr_of_nodes):
                for j in range(self.nr_of_nodes):
                    if matrix[i][k] and matrix[k][j] and i != j:
                        if matrix[i][j] > matrix[i][k]+matrix[k][j] or matrix[i][j] == 0:
                            matrix[i][j] = matrix[i][k]+matrix[k][j]
        return matrix


f = open("graph.in", "r")
f_out = open("graph.out", "w")
values = [int(z) for z in f.readline().split()]
if len(values) == 1:
    N = values[0]
    M = N
elif len(values) == 2:
    N, M = values[0], values[1]
else:
    N, M, S = values[0], values[1], values[2]
my_graph = Graph(N)
my_matrix = my_graph.read_weighted_directed_graph_royfloyd(M)
my_matrix = my_graph.royfloyd(my_matrix)
for values in my_matrix:
    for value in values:
        f_out.write(str(value) + " ")
    f_out.write("\n")
