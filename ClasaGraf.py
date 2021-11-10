import copy
import random
from collections import deque


# function to remove a node from a graph
def remove_node(this_graph, delete_value):
    if delete_value in this_graph:
        del this_graph[delete_value]
    for edges in this_graph.values():
        copy_edge = copy.deepcopy(edges)
        if delete_value in copy_edge:
            edges.remove(delete_value)


# deep first search for this graph
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


class Graph:

    # initialize the graph
    def __init__(self, nr_nodes):
        # dictionary to store graph
        self.graph = {}

        # list of nodes
        self.my_nodes = [x for x in range(1, nr_nodes + 1)]

        # No. of nodes
        self.nodes = nr_nodes

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

    # read the undirected graph from input file
    def read_undirected_graph(self, nr_edges):
        for i in range(nr_edges):
            x, y = [int(z) for z in f.readline().split()]
            self.add_edge(x, y)
            self.add_edge(y, x)

    # read the directed graph from input file
    def read_directed_graph(self, nr_edges):
        for i in range(nr_edges):
            x, y = [int(z) for z in f.readline().split()]
            self.add_edge(x, y)

    # get the shortest distance from starting node to each node in distance with breath first search
    def bfs(self, starting_node):
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


f = open("graph.in", "r")
f_out = open("graph.out", "w")
values = [int(z) for z in f.readline().split()]
if len(values) == 2:
    N, M = values[0], values[1]
else:
    N, M, S = values[0], values[1], values[2]
my_graph = Graph(N)
my_graph.read_directed_graph(M)
