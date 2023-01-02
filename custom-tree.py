import json
from treelib import Tree
from copy import deepcopy

"""Utils function for custom tree.

    The custom tree is defined as a dictionary.
    Each entry of the dictionary is a node of the tree.
    Each node is itself a dictionary with three keys:
    * parent: dictionary of the parents of the node.
    * children: dictionary of the children of the node.
    * value: the value of the node.

    Note that the root of the tree has no parent.
    Note that the parent of a node is a list of one element.

    Each element of the parent or children dictionary is an edge between current node and target node.
    Keys of the dictionary are the target node.
    
    This structure is compatible with the treelib library via the get_tree_layout function.
        
    Example of a tree:
    
    edge12 = 'edge12'
    edge21 = 'edge21'
    edge13 = 'edge13'
    edge24 = 'edge24'
    edge25 = 'edge25'
    edge31 = 'edge31'
    edge42 = 'edge42'
    edge52 = 'edge52'
    
    tree = {'1': {'parent': {}, 'children': {'2': edge12, '3': edge13}, 'val': val1},
            '2': {'parent': {'1': edge21}, 'children': {'4': edge24, '5': edge25}, 'val': val2},
            '3': {'parent': {'1': edge31}, 'children': {}, 'val': val3},
            '4': {'parent': {'2': edge42}, 'children': {}, 'val': val4},
            '5': {'parent': {'2': edge52}, 'children': {}, 'val': val5},
            }
    """


def get_root(tree):
    for node in tree:
        if tree[node]['parent'] == {}:
            return node


def get_children(tree, node):
    return tree[node]['children']


def get_parent(tree, node):
    return tree[node]['parent']


def recursive_tree(tree, tree_out, node):
    """Recursive function to create a tree with the treelib library."""
    children = get_children(tree, node)
    if children == {}:
        return
    for child in children:
        tree_out.create_node(child, child, parent=node)
        recursive_tree(tree, tree_out, child)
    return tree, tree_out


def get_tree_layout(tree):
    """Create a tree with the treelib library from a custom tree."""
    root = get_root(tree)
    tree_out = Tree()
    tree_out.create_node(root, root)
    tree, tree_out = recursive_tree(tree, tree_out, root)
    return tree_out


def get_path(tree, node):
    """Get the path from the root to the node id.
    The root is the first element of the list.
    The target node is the last element of the list."""
    path = []
    while node != {}:
        if isinstance(node, str):
            node_up = node
        else:
            node_up = list(node.keys())[0]
        path.append(node_up)
        node = get_parent(tree, node_up)
    path = path[::-1]
    return path


def get_edges(tree, node):
    """Get a comprehensive path of ascending/descending edges from the root to a target node.
    The output is a list `edges`.
    The length of `edges` is the number of edges to go from the root to the target node.
    Each element of path is a dict with two keys:
    *'forward': the descending edge (from the parent to the child).
    *'backward': the ascending edge (from the child to the parent).

    Args:
        tree (dict): custom tree.
        node (str): target node

    Returns:
        edge (list): list of the ascending/desceding edges from the root to the target node.        
    """

    path = get_path(tree, node)
    edges = [None] * (len(path) - 1)
    for k in range(len(path) - 1):
        node1 = path[k]
        node2 = path[k + 1]
        edge12 = get_children(tree, node1)[node2]
        edge21 = get_parent(tree, node2)[node1]
        edges[k] = {'forward': edge12, 'backward': edge21}
    return edges


def update_tree(tree, node, edges):
    """Update the tree with the new edges."""
    tree_old = deepcopy(tree)
    path = get_path(tree, node)
    if len(edges) != len(path) - 1:
        raise ValueError(
            'The number of new edges does not match the expected number of edges to replace.')
    for k in range(len(path) - 1):
        node1 = path[k]
        node2 = path[k + 1]
        tree[node1]['children'][node2] = edges[k]['forward']
        tree[node2]['parent'][node1] = edges[k]['backward']
    return tree, tree_old


def remove_edge(dictionary, edge):
    dic_out = {key: val for key, val in dictionary.items() if val != edge}
    return dic_out


def exchange_arrow(tree, node1_id, node2_id):
    """Exchange the arrow between two nodes.
    This means that we exchange the role of parent/child between the two nodes.

    Args:
        tree (dict): custom tree.
        node1_id (str): id of the first node (parent of node2).
        node2_id (str): id of the second node (child of node1).

    Returns:
        tree (dict): custom tree with the arrow exchanged.
    """
    children_node_1 = get_children(tree, node1_id)
    children_node_2 = get_children(tree, node2_id)
    parent_node_1 = get_parent(tree, node1_id)
    parent_node_2 = get_parent(tree, node2_id)

    edge12 = children_node_1[node2_id]
    edge21 = parent_node_2[node1_id]

    children_node_1 = remove_edge(children_node_1, edge12)
    parent_node_2 = remove_edge(parent_node_2, edge21)
    children_node_2[node1_id] = edge21
    parent_node_1[node2_id] = edge12

    tree[node1_id]['parent'] = parent_node_1
    tree[node2_id]['parent'] = parent_node_2
    tree[node1_id]['children'] = children_node_1
    tree[node2_id]['children'] = children_node_2

    return tree


def invert_tree_path(tree, path):
    for i in range(len(path)-1):
        tree = exchange_arrow(tree, path[i], path[i+1])
    return tree


def change_root(tree, node):
    """Change the root of the tree."""
    tree_old = deepcopy(tree)
    path = get_path(tree, node)
    tree = invert_tree_path(tree, path)
    return tree, tree_old


if __name__ == '__main__':
    val1 = 'val1'
    val2 = 'val2'
    val3 = 'val3'
    val4 = 'val4'
    val5 = 'val5'

    edge12 = 'edge12'
    edge21 = 'edge21'
    edge13 = 'edge13'
    edge24 = 'edge24'
    edge25 = 'edge25'
    edge31 = 'edge31'
    edge42 = 'edge42'
    edge52 = 'edge52'

    tree = {'1': {'parent': {}, 'children': {'2': edge12, '3': edge13}, 'val': val1},
            '2': {'parent': {'1': edge21}, 'children': {'4': edge24, '5': edge25}, 'val': val2},
            '3': {'parent': {'1': edge31}, 'children': {}, 'val': val3},
            '4': {'parent': {'2': edge42}, 'children': {}, 'val': val4},
            '5': {'parent': {'2': edge52}, 'children': {}, 'val': val5},
            }
    tree_layout_old = get_tree_layout(tree)
    print('\n \n Old tree layout: \n')
    tree_layout_old.show(line_type='ascii-em')    
    # The function also works if we choose node_id to be the current root
    node_id = '5'
    edges = get_edges(tree, node_id)
    edges[0]['backward'] = 'edge21new'
    edges[1]['backward'] = 'edge52new'
    tree_update, tree_old = update_tree(tree, node_id, edges)
    tree_change, tree_update = change_root(tree_update, node_id)
    tree_layout = get_tree_layout(tree_change)
    #print('Updated tree structure (new edges and root changed): \n{}'.format(
    #    json.dumps(tree_change, indent=4)))
    print('\n \n Updated tree layout: \n')
    tree_layout.show(line_type='ascii-em')
