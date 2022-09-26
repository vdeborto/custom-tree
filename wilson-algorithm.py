import random


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


def custom_graph_layout(graph):
    return graph_layout


if __name__ == "__main__":
    graph = {'1': ['2', '3'], '2': ['1', '3'], '3': ['1', '2']}
    parent = random_spanning_tree(graph)
    print(parent)
