"""
Searches module defines all different search algorithms
"""
from graph import graph as g

def bfs(graph, initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    queue = []
    edges = []

    queue.append([initial_node])

    while queue:
        path = queue.pop(0)
        node = path[-1]

        if node == dest_node:
            # find edges given the nodes in path
            for i, node in enumerate(path):
                if i < len(path) - 1:
                    edge = g.Edge(node, path[i + 1], graph.distance(node, path[i + 1]))
                    edges.append(edge)
            return edges

        for neighbor in graph.neighbors(node):
            new_path = list(path)
            new_path.append(neighbor)
            queue.append(new_path)

def dfs(graph, initial_node, dest_node):
    """
    Depth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    pass

def dijkstra_search(graph, initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    pass

def a_star_search(graph, initial_node, dest_node):
    """
    A* Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    pass
