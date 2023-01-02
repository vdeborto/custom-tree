from typing import Any

class Graph():
    def __init__(self, n_vertices) -> None:
        self.n_vertices = n_vertices
        self.graph = [{} for _ in range(n_vertices)]

    def add_edge(self, source: int, destination: int, source_destination: Any, destination_source: Any):
        """Create an edge between `source` and `destination`.
        The value of the edge going from `source` to `destination` is `source_destination`.
        The value of the edge going from `destination` to `source` is `destination_source`.  
        
        Args:
            source (int): source index.
            destination (int): destination index.
            source_destination (Any): value of the outgoing edge.
            destination_source (Any): value of the ingoing edge.
        """
        self.graph[source][destination] = (source_destination, destination_source)
        
    def __str__(self):
        strout = ''
        for idx in range(self.n_vertices):
            if self.graph[idx]:
                strout += f'Node {idx} has children '
                for destination in self.graph[idx].keys():
                    strout += f'{destination}, '
                strout = strout[:-2] + '.\n'
        return strout
    
def get_leaves(graph: Graph) -> set[int]:
    """Get the set of leaves of a graph."""
    out = set()
    for i in range(len(graph.graph)):
        if not graph.graph[i]: out.add(i)
    return out

def get_root(graph: Graph) -> int:
    """Get the root of a graph. (graph is assumed to be a tree)"""
    nodes = set(list(range(graph.n_vertices)))
    nodes_children = set()
    for children in graph.graph:
        nodes_children = nodes_children.union(set(children.keys()))
    out = nodes.difference(nodes_children)
    return list(out)[0]

def find_path_rec(graph: Graph, lst: list[int], root: int, target: int) -> bool:
    if root == target: 
        lst.append(target)
        return True
    for child in graph.graph[root].keys():
        out = find_path_rec(graph, lst, child, target)
        if out:
            lst.append(root)
            return True
    return False

def find_path(graph: Graph, root: int, target: int) -> list[int]:
    """Find a path between `root` and `target`.
    Note that root is not necessarily the root of `graph`."""
    lst = []
    find_path_rec(graph, lst, root, target)
    return lst[::-1]

def revert_path_rec(graph: Graph, path: list[int], idx: int):
    if idx >= (len(path)-1): return graph
    source, destination = path[idx], path[idx+1]
    val = graph.graph[source].pop(destination)
    graph.graph[destination][source] = (val[1],val[0])
    revert_path_rec(graph, path, idx+1)

def revert_path(graph: Graph, path: list[int]):
    """Inplace reversal of the edges along a path."""
    revert_path_rec(graph, path, 0)

def change_root(graph: Graph, new_root: int):
    """Inplace change of the root of a tree."""
    root = get_root(graph)
    path = find_path(graph, root, new_root)
    revert_path(graph, path)

if __name__=='__main__':    
    
    graph = Graph(6)
    graph.add_edge(0, 1, '01','10')
    graph.add_edge(0, 2, '02','20')
    graph.add_edge(1, 3, '13','31')
    graph.add_edge(3, 4, '34','43')
    graph.add_edge(3, 5, '35','53')
    
    print(graph)
    print(f'Leaves of the graph are {get_leaves(graph)}.')
    print(f'Root of the graph is {get_root(graph)}. \n \n \n')
    
    change_root(graph, 5)
    print(graph)
    print(f'Leaves of the graph are {get_leaves(graph)}.')
    print(f'Root of the graph is {get_root(graph)}.')    