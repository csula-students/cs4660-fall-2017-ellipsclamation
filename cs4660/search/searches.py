"""
Searches module defines all different search algorithms
"""
from graph import graph as g
try:
    import Queue as q
except ImportError:
    import queue as q

def bfs(graph, initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    queue = []
    actions = []

    queue.append([initial_node])

    while queue:
        path = queue.pop(0)
        # last node in path
        node = path[-1]

        if node == dest_node:
            # convert nodes to edges
            for i in range(len(path) - 1):
                edge = g.Edge(path[i], path[i + 1], graph.distance(path[i], path[i + 1]))
                actions.append(edge)
            return actions

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

    actions = []
    child = dest_node

    # convert nodes to edges
    while child != initial_node:
        parent = parents[child]
        actions = [g.Edge(parent, child, graph.distance(parent, child))] + actions
        child = parent

    return actions

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
    dist = {}
    prev = {}
    dist[initial_node] = 0
    queue = []
    actions = []

    queue.append((0, initial_node))

    while queue:
        # remove and return best vertex
        node = queue.pop(0)[1]

        for neighbor in graph.neighbors(node):
            alt = dist[node] + graph.distance(node, neighbor)

            if neighbor not in dist or alt < dist[neighbor]:
                queue.append((alt, neighbor))
                dist[neighbor] = alt
                prev[neighbor] = node

        # sort
        queue = sorted(queue, key=lambda priority: priority[0])

    current = dest_node

    # convert nodes to edges
    while current != initial_node:
        parent = prev[current]
        actions = [g.Edge(parent, current, graph.distance(parent, current))] + actions
        current = parent

    return actions

def a_star_search(graph, initial_node, dest_node):
    """
    A* Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    frontier = q.PriorityQueue()
    explored_set = {}
    parents = {}
    g_score = {}
    f_score = {}
    actions = []

    frontier.put(PriorityEntry(0, initial_node))

    g_score[initial_node] = 0
    f_score[initial_node] = heuristic(initial_node, dest_node)

    while frontier:
        current = frontier.get().data

        if current in explored_set:
            continue

        if current == dest_node:
            while current != initial_node:
                parent = parents[current]
                actions = [g.Edge(parent, current, graph.distance(parent, current))] + actions
                current = parent

            return actions

        explored_set[current] = True

        for neighbor in graph.neighbors(current):
            if neighbor in explored_set:
                continue

            temp_g_score = g_score[current] + graph.distance(current, neighbor)

            if neighbor in g_score and temp_g_score >= g_score[neighbor]:
                continue

            parents[neighbor] = current
            g_score[neighbor] = temp_g_score
            f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, dest_node)
            frontier.put(PriorityEntry(f_score[neighbor], neighbor))

    return actions

def heuristic(a, b):
    D = 1.8
    dx = abs(a.data.x - b.data.x)
    dy = abs(a.data.y - b.data.y)
    return D * (dx ** 2 + dy ** 2) ** 0.5

class PriorityEntry(object):
    def __init__(self, priority, data):
        self.data = data
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority
