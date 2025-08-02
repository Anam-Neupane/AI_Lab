from collections import deque

def dfs(graph, start_node):
    """
    Performs a Depth-First Search (DFS) on a graph.

    Args:
        graph (dict): A dictionary representing the graph where keys are nodes
                      and values are lists of their neighbors.
        start_node: The node from which to start the DFS.

    Returns:
        list: A list of nodes in the order they were visited during the DFS.
    """
    if start_node not in graph:
        raise ValueError(f"Start node '{start_node}' not found in the graph.")

    visited = set()  # To keep track of visited nodes
    stack = deque()  # Stack for DFS (LIFO)

    visited.add(start_node)
    stack.append(start_node)
    
    traversal_order = []

    while stack:
        current_node = stack.pop()  # Pop from the stack (LIFO)
        traversal_order.append(current_node)

        # Explore neighbors in reverse to maintain consistent order
        for neighbor in reversed(graph.get(current_node, [])):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
    
    return traversal_order

# --- Example Usage ---

if __name__ == "__main__":
    # Example 1: Simple Graph
    graph1 = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    print("DFS Traversal for Graph 1 (starting from 'A'):")
    print(dfs(graph1, 'A'))  # Example: ['A', 'B', 'D', 'E', 'F', 'C']

    # Example 2: Disconnected Graph
    graph2 = {
        '1': ['2', '3'],
        '2': ['1', '4'],
        '3': ['1', '5'],
        '4': ['2'],
        '5': ['3'],
        '6': ['7'],
        '7': ['6']
    }
    print("\nDFS Traversal for Graph 2 (starting from '1'):")
    print(dfs(graph2, '1'))  # Example: ['1', '2', '4', '3', '5']

    # Example 3: Single node graph
    graph3 = {
        'X': []
    }
    print("\nDFS Traversal for Graph 3 (starting from 'X'):")
    print(dfs(graph3, 'X'))  # Expected: ['X']

    # Example 4: Empty graph
    graph4 = {}
    try:
        print("\nDFS Traversal for Graph 4 (starting from 'Z'):")
        print(dfs(graph4, 'Z'))
    except ValueError as e:
        print(e)
