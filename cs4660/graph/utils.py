"""
utils package is for some quick utility methods

such as parsing
"""

from . import graph as g

class Tile(object):
    """Node represents basic unit of graph"""
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

    def __str__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)
    def __repr__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y and self.symbol == other.symbol
        return False
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self.x) + "," + str(self.y) + self.symbol)



def parse_grid_file(graph, file_path):
    """
    ParseGridFile parses the grid file implementation from the file path line
    by line and construct the nodes & edges to be added to graph

    Returns graph object
    """
    # TODO: read the filepath line by line to construct nodes & edges

    # TODO: for each node/edge above, add it to graph

    # each row contains list of 2 character tiles of the row
    rows = []

    with open(file_path) as f:
        for line in f:
            # skips borders
            if line[0] == '+':
                continue
            # omits | at beginning and end of row
            grid_content = line[1:-2]
            rows.append([grid_content[i:i+2] for i in range(0, len(grid_content), 2)])

    # row
    y = 0

    for row in rows:
        # column
        x = 0

        for tile in row:
            # skips adding walls as node
            if tile == '##':
                x += 1
                continue

            curr_tile = g.Node(Tile(x, y, tile))

            graph.add_node(curr_tile)

            # add top edge
            if y > 0 and Tile(x, y - 1, rows[y - 1][x]).symbol != '##':
                top_tile = g.Node(Tile(x, y - 1, rows[y - 1][x]))
                graph.add_edge(g.Edge(curr_tile, top_tile, 1))

            # add right edge
            if x < len(row) - 1 and Tile(x + 1, y, rows[y][x + 1]).symbol != '##':
                right_tile = g.Node(Tile(x + 1, y, rows[y][x + 1]))
                graph.add_edge(g.Edge(curr_tile, right_tile, 1))

            # add bottom edge
            if y < len(rows) - 1 and Tile(x, y + 1, rows[y + 1][x]).symbol != '##':
                bot_tile = g.Node(Tile(x, y + 1, rows[y + 1][x]))
                graph.add_edge(g.Edge(curr_tile, bot_tile, 1))

            # add left edge
            if x > 0 and Tile(x - 1, y, rows[y][x - 1]).symbol != '##':
                left_tile = g.Node(Tile(x - 1, y, rows[y][x - 1]))
                graph.add_edge(g.Edge(curr_tile, left_tile, 1))

            x += 1
        y += 1

    return graph

def convert_edge_to_grid_actions(edges):
    """
    Convert a list of edges to a string of actions in the grid base tile

    e.g. Edge(Node(Tile(1, 2), Tile(2, 2), 1)) => "S"
    """
    actions = ""

    for edge in edges:
        # North
        if edge.from_node.data.y > edge.to_node.data.y:
            actions += "N"
        # East
        elif edge.from_node.data.x < edge.to_node.data.x:
            actions += "E"
        # South
        elif edge.from_node.data.y < edge.to_node.data.y:
            actions += "S"
        # West
        elif edge.from_node.data.x > edge.to_node.data.x:
            actions += "W"

    return actions