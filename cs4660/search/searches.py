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
        # last node in path
        node = path[-1]

        if node == dest_node:
            # convert nodes to edges
            for i in range(len(path) - 1):
                edge = g.Edge(path[i], path[i + 1], graph.distance(path[i], path[i + 1]))
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
    parents = {}

    dfs_helper(graph, initial_node, {}, parents)

    edges = []
    child = dest_node

    # convert nodes to edges
    while child != initial_node:
        parent = parents[child]
        edges = [g.Edge(parent, child, graph.distance(parent, child))] + edges
        child = parent

    return edges

def dfs_helper(graph, current, is_discovered, parents):
    for child in graph.neighbors(current):
        if child in is_discovered:
            continue
        is_discovered[child] = True
        parents[child] = current
        dfs_helper(graph, child, is_discovered, parents)

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
