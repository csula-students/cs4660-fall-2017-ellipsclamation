"""
quiz2!

Use path finding algorithm to find your way through dark dungeon!

Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9

TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""

import json
import codecs
from graph import graph as g
from search import searches

try:
    import Queue as queue
except ImportError:
    import queue

# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"

def get_state(room_id):
    """
    get the room by its id and its neighbor
    """
    body = {'id': room_id}
    return __json_request(GET_STATE_URL, body)

def transition_state(room_id, next_room_id):
    """
    transition from one room to another to see event detail from one room to
    the other.

    You will be able to get the weight of edge between two rooms using this method
    """
    body = {'id': room_id, 'action': next_room_id}
    return __json_request(STATE_TRANSITION_URL, body)

def __json_request(target_url, body):
    """
    private helper method to send JSON request and parse response JSON
    """
    req = Request(target_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    reader = codecs.getreader("utf-8")
    response = json.load(reader(urlopen(req, jsondataasbytes)))
    return response

def path_to_strings(actions):
    path = []
    total_weight = 0

    for action in actions:
        from_node_string = str(get_state(action.from_node.data)['location']['name']) + "(" + str(action.from_node.data) + ")"
        to_node_string = str(get_state(action.to_node.data)['location']['name']) + "(" + str(action.to_node.data) + ")"
        weight = action.weight
        total_weight += weight
        path.append(from_node_string + ":" + to_node_string + ":" + str(weight))

    return path, str(total_weight)

def bfs_path(initial_node, dest_node):
    actions = bfs(initial_node, dest_node)
    return path_to_strings(actions)

def dijkstra_path(initial_node, dest_node):
    actions = dijkstra_search(initial_node, dest_node)
    return path_to_strings(actions)

def bfs(initial_node, dest_node):
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
                edge = g.Edge(path[i], path[i + 1], transition_state(path[i].data, path[i + 1].data)['event']['effect'])
                actions.append(edge)
            return actions

        for neighbor_room in get_state(node.data)['neighbors']:
            neighbor = g.Node(neighbor_room['id'])
            new_path = list(path)
            new_path.append(neighbor)
            queue.append(new_path)

def dijkstra_search(initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    dist = {}
    prev = {}
    queue = []
    actions = []
    visited = []

    dist[initial_node] = 0
    queue.append((0, initial_node))

    while queue:
        node = queue.pop(0)[1]
        visited.append(node)

        current_room = get_state(node.data)
        for neighbor_room in current_room['neighbors']:
            neighbor = g.Node(neighbor_room['id'])
            alt = dist[node] - transition_state(node.data, neighbor.data)['event']['effect']

            if neighbor not in dist or (alt < dist[neighbor] and neighbor not in visited):
                queue.append((alt, neighbor))
                dist[neighbor] = alt
                prev[neighbor] = node

        # sort
        queue = sorted(queue, key=lambda priority: priority[0])

    current = dest_node

    # convert nodes to edges
    while current != initial_node:
        parent = prev[current]
        actions = [g.Edge(parent, current, transition_state(parent.data, current.data)['event']['effect'])] + actions
        current = parent

    return actions

if __name__ == "__main__":
    # Your code starts here
    empty_room_node = g.Node(get_state('7f3dc077574c013d98b2de8f735058b4')['id'])
    dark_room_node = g.Node(get_state('f1f131f647621a4be7c71292e79613f9')['id'])

    strings = bfs_path(empty_room_node, dark_room_node)
    print("BFS path:")
    for actions in strings[0]:
        print(actions)
    print("Total hp: " + strings[1])

    strings = dijkstra_path(empty_room_node, dark_room_node)
    print("\nDijkstra path:")
    for actions in strings[0]:
        print(actions)
    print("Total hp: " + strings[1])
