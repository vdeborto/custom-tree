import random

"""Utils function for custom graph.

    The custom tree is defined as an adjacency dictionary.
    Each entry of the dictionary is a node of the graph.
    Each node is itself a dictionary with two keys:
    * neighbors: dictionary of the neighbors of the node.
    * value: the value of the node.

    Each element of the parent or children dictionary is an edge between current node and target node.
    Keys of the dictionary are the target node.
            
    Example of a graph:
    
    val1 = 'val1'
    val2 = 'val2'
    val3 = 'val3'
    
    edge12 = 'edge12'
    edge21 = 'edge21'
    edge13 = 'edge13'
    edge23 = 'edge23'
    
    graph = {'1': {'neighbors': {'2': edge12, '3': edge13}, 'val': val1},
            '2': {'neighbors': {'1': edge21, '3': edge23}, 'val': val2},
            '3': {'neighbors': {'1': edge31, '2': edge32}, 'val': val3},
            }
    """


def random_spanning_tree(graph):
    """Return uniform random spanning tree of undirected graph.
    """
    root = random.choice(list(graph))
    parent = {root: None}
    tree = set([root])
    for vertex in graph:

        # Take random walk from a vertex to the tree.
        v = vertex
        while v not in tree:
            neighbor = random.choice(graph[v])
            parent[v] = neighbor
            v = neighbor

        # Erase any loops in the random walk.
        v = vertex
        while v not in tree:
            tree.add(v)
            v = parent[v]  # implicit erasure of loop
    return parent


def custom_to_layout(graph):
    graph_layout = {}
    for node in graph:
        neighbors = graph[node]['neighbors']
        graph_layout[node] = list(neighbors.keys())
    return graph_layout


def parent_to_custom_tree(graph, parent):


if __name__ == "__main__":

    val1 = 'val1'
    val2 = 'val2'
    val3 = 'val3'

    edge12 = 'edge12'
    edge21 = 'edge21'
    edge13 = 'edge13'
    edge23 = 'edge23'
    edge31 = 'edge31'
    edge32 = 'edge32'

    graph = {'1': {'neighbors': {'2': edge12, '3': edge13}, 'val': val1},
             '2': {'neighbors': {'1': edge21, '3': edge23}, 'val': val2},
             '3': {'neighbors': {'1': edge31, '2': edge32}, 'val': val3},
             }

    graph_layout = custom_graph_layout(graph)
    print(graph_layout)
    parent = random_spanning_tree(graph_layout)
    print(parent)
