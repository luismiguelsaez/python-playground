from queue import PriorityQueue

class Graph():
    def __init__(self, num_of_vertices):
        self.v = num_of_vertices
        # Initialize edges matrix
        self.edges = [[-1 for i in range(num_of_vertices)] for j in range(num_of_vertices)]
        # Initialize visited vertices list
        self.visited = []
        
    def add_edge(self, u, v, weight):
        self.edges[u][v] = weight
        self.edges[v][u] = weight

    def dijkstra(self, graph, start_vertex):
        # Initialize the list to keep the path lengths from start vertex
        D = {v: float('inf') for v in range(graph.v)}
        D[start_vertex] = 0
        
        # Create the queue and put the distance for the start vertex
        # The queue sorts the vertices from least to most distant
        pq = PriorityQueue()
        pq.put((0, start_vertex))
        
        while not pq.empty():
            (dist, current_vertex) = pq.get()
            graph.visited.append(current_vertex)
            
            for neighbor in range(graph.v):
                if graph.edges[current_vertex][neighbor] != -1:
                    distance = graph.edges[current_vertex][neighbor]
                    if neighbor not in graph.visited:
                        old_cost, new_cost = D[neighbor], D[current_vertex] +  distance
                        if new_cost < old_cost:
                            pq.put((new_cost, neighbor))
                            D[neighbor] = new_cost
        
        return D

g = Graph(9)
g.add_edge(0, 1, 4)
g.add_edge(0, 6, 7)
g.add_edge(1, 6, 11)
g.add_edge(1, 7, 20)
g.add_edge(1, 2, 9)
g.add_edge(2, 3, 6)
g.add_edge(2, 4, 2)
g.add_edge(3, 4, 10)
g.add_edge(3, 5, 5)
g.add_edge(4, 5, 15)
g.add_edge(4, 7, 1)
g.add_edge(4, 8, 5)
g.add_edge(5, 8, 12)
g.add_edge(6, 7, 1)
g.add_edge(7, 8, 3)

D = g.dijkstra(g, 0)

print(D)