import copy
import random
import sys
from collections import deque


class Graph:
    # List of functions :
    # 1. dfs_connected : find the number of connected components for a graph in my class
    # 2. bfs_shortest : get the shortest distance from starting node to each node in distance with bfs
    # 3. find_ctc_components : function to find strongly connected component in a directed graph
    # 4. find_topological_order : function to find topological order in a directed acyclic graph
    # 5. find_articulation_edge : function to find critical connections in a graph
    # 6. dijkstra : function to use Dijkstra's algorithm from node 1
    # 7. bellman_ford : function to use Bellman-Ford algorithm
    # 8. kruskal : function to use Kruskal algorithm
    # 9. diameter_tree : length of the farthest distance from two nodes of a tree
    # 10. royfloyd : Floyd–Warshall/Roy-Floyd algorithm
    # 11. eulerian : find the Eulerian path

    # initialize the graph
    def __init__(self, nr_nodes):
        self.graph = {}  # dictionary to store graph
        self.my_nodes = [x for x in range(1, nr_nodes + 1)]
        self.nr_of_nodes = nr_nodes  # No. of nodes

    # !! PRIVATE FUNCTIONS !!

    def change_nodes(self):
        if 0 in self.graph.keys():
            self.my_nodes = [x for x in range(0, self.nr_of_nodes)]  # list of nodes

    # function to add an edge to graph
    def add_edge(self, node1, node2):
        if node1 not in self.graph:
            self.graph[node1] = [node2]
        elif node1 in self.graph:
            self.graph[node1].append(node2)

    # function to delete an edge from graph
    def del_edge(self, node1, node2):
        if node1 in self.graph:
            self.graph[node1].remove(node2)

    def del_weighted_edge(self, node1, node2, weight):
        if node1 in self.graph:
            item = (node2, weight)
            self.graph[node1].remove(item)

    # function to remove a node from a graph
    def remove_node(self, delete_value):
        if delete_value in self.graph:
            del self.graph[delete_value]
        for edges in self.graph.values():
            copy_edge = copy.deepcopy(edges)
            if delete_value in copy_edge:
                edges.remove(delete_value)

    # function to add a weighted edge to graph
    def add_weighted_edge(self, node1, node2, weight):
        temp = (node2, weight)
        if node1 not in self.graph:
            self.graph[node1] = [temp]
        elif node1 in self.graph:
            self.graph[node1].append(temp)

    # !! PUBLIC FUNCTIONS !!

    # read the unweighted, undirected graph from input file
    def read_unweighted_undirected_graph(self, nr_edges):
        for i in range(nr_edges):
            x, y = [int(z) for z in f.readline().split()]
            if x == y:
                self.add_edge(x, y)
            else:
                self.add_edge(x, y)
                self.add_edge(y, x)
        self.change_nodes()

    # read the unweighted, directed graph from input file
    def read_unweighted_directed_graph(self, nr_edges):
        for i in range(nr_edges):
            x, y = [int(z) for z in f.readline().split()]
            if x == y:
                self.add_edge(x, y)
            else:
                self.add_edge(x, y)
        self.change_nodes()

    # read the weighted, undirected graph from input file
    def read_weighted_undirected_graph(self, nr_edges):
        for i in range(nr_edges):
            x, y, w = [int(z) for z in f.readline().split()]
            if x == y:
                self.add_weighted_edge(x, y, w)
            else:
                self.add_weighted_edge(x, y, w)
                self.add_weighted_edge(y, x, w)
        self.change_nodes()

    # read the weighted, directed graph from input file
    def read_weighted_directed_graph(self, nr_edges):
        for i in range(nr_edges):
            x, y, w = [int(z) for z in f.readline().split()]
            if x == y:
                self.add_weighted_edge(x, y, w)
            else:
                self.add_weighted_edge(x, y, w)
        self.change_nodes()

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
        self.change_nodes()
        return matrix

    # read the unweighted, undirected graph from input file
    def read_unweighted_undirected_bipartite_graph(self, nr_edges, cardinal):
        for i in range(nr_edges):
            x, y = [int(z) for z in f.readline().split()]
            self.add_edge(x, y + cardinal)
            self.add_edge(y + cardinal, x)
        self.change_nodes()

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

    def weighted_dfs(self, starting_node):
        stack, result = [(starting_node, 0)], []
        while stack:
            node = stack.pop()
            same_node = 0
            for pair in result:
                if node[0] == pair[0]:
                    same_node = 1
                    break
            if same_node == 1:
                continue
            result.append(node)
            if node[0] in self.graph:
                for node1 in self.graph[node[0]]:
                    stack.append(node1)
        return result

    def dfs_edges(self, starting_node):
        stack, result = [starting_node], []
        copy_graph = Graph(self.nr_of_nodes)
        copy_graph.graph = copy.deepcopy(self.graph)
        while stack:
            node = stack.pop()
            if node in result:
                continue
            if len(result) >= 1:
                if node in copy_graph.graph[result[-1]]:
                    copy_graph.del_edge(result[-1], node)
                    copy_graph.del_edge(node, result[-1])
                else:
                    for vertex in result:
                        if node in copy_graph.graph[vertex]:
                            copy_graph.del_edge(vertex, node)
                            copy_graph.del_edge(node, vertex)
                            break
            result.append(node)
            if node in self.graph:
                for node1 in self.graph[node]:
                    stack.append(node1)
        return result, copy_graph

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
        return len(components)

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
        trans_graph = Graph(self.nr_of_nodes)
        for node, edges in self.graph.items():
            for node2 in edges:
                trans_graph.add_edge(node2, node)
        ctc = []
        copy_graph = copy.deepcopy(self.graph)
        while self.graph:
            nod = random.choice(list(self.graph.keys()))
            result_dfs = self.dfs(nod)
            trans_result_dfs = trans_graph.dfs(nod)
            plus_minus = list(set(result_dfs) & set(trans_result_dfs))
            ctc.append(plus_minus)
            for member in plus_minus:
                self.remove_node(member)
                trans_graph.remove_node(member)
        # if keys are left in trans_adj_list then they are from ctc
        for nod in trans_graph.graph.keys():
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
                    self.remove_node(node_to_remove)
        for node, income in incoming_degree.items():
            if income == 0:
                topological_order.append(node)
        self.graph = copy.deepcopy(copy_graph)
        return topological_order

    # Part I : Critical Connections in a Network
    # function to find critical connections in a graph
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
                            result_dfs = self.dfs(nod)
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

    # Part IV : ciclueuler
    # Find the Eulerian path
    def eulerian(self, node):
        for current_node, neighbours in self.graph.items():
            if current_node in neighbours:
                counter = neighbours.count(current_node)
                print(current_node, counter)
                degree = len(neighbours) - counter
            else:
                degree = len(neighbours)
            if degree % 2 != 0:
                return -1
        result_dfs, back_edges = self.dfs_edges(node)
        cycle = [result_dfs[0]]
        current_node = result_dfs[0]
        while any([self.graph[i] != [] for i in self.graph]):
            if not back_edges.graph[current_node]:
                for vertex in result_dfs:
                    if vertex in self.graph[current_node]:
                        if current_node != vertex:
                            self.del_edge(current_node, vertex)
                            self.del_edge(vertex, current_node)
                        else:
                            self.del_edge(current_node, vertex)
                        current_node = vertex
                        cycle.append(vertex)
                        break
            else:
                for vertex in result_dfs:
                    if vertex in back_edges.graph[current_node]:
                        if current_node != vertex:
                            self.del_edge(current_node, vertex)
                            self.del_edge(vertex, current_node)
                            back_edges.del_edge(current_node, vertex)
                            back_edges.del_edge(vertex, current_node)
                        else:
                            self.del_edge(current_node, vertex)
                            back_edges.del_edge(current_node, vertex)
                        current_node = vertex
                        cycle.append(vertex)
                        break
        cycle.pop()
        return cycle

    # Part IV : hamilton
    # Find the hamiltonian cycle of the lowest cost
    def hamilton(self, node):
        copy_graph = Graph(self.nr_of_nodes)
        copy_graph.my_nodes = copy.deepcopy(self.my_nodes)
        copy_graph.graph = copy.deepcopy(self.graph)
        while self.graph[node]:
            minimum_cost = 0
            result_dfs = self.weighted_dfs(node)
            print(result_dfs)
            self.del_weighted_edge(node, result_dfs[1][0], result_dfs[1][1])
            print(self.graph)
            return minimum_cost

    # Part IV : cuplaj
    # Find a maximum matching in a bipartite graph


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
my_graph.read_weighted_directed_graph(M)
print(my_graph.graph)
print(my_graph.my_nodes)
hamilton = my_graph.hamilton(1)
if hamilton == 0:
    f_out.write("Nu exista solutie")
else:
    f_out.write(str(hamilton))

