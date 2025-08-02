from collections import deque

def bfs(graph, start_node):
    """
    Performs a Breadth-First Search (BFS) on a graph.

    Args:
        graph (dict): A dictionary representing the graph where keys are nodes
                      and values are lists of their neighbors.
        start_node: The node from which to start the BFS.

    Returns:
        list: A list of nodes in the order they were visited during the BFS.
    """
    if start_node not in graph:
        raise ValueError(f"Start node '{start_node}' not found in the graph.")

    visited = set()  # To keep track of visited nodes
    queue = deque()  # A queue for nodes to visit

    visited.add(start_node)
    queue.append(start_node)
    
    traversal_order = []

    while queue:
        current_node = queue.popleft()  # Dequeue the first node
        traversal_order.append(current_node)

        # Explore neighbors
        for neighbor in graph.get(current_node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
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
    print("BFS Traversal for Graph 1 (starting from 'A'):")
    print(bfs(graph1, 'A'))  # Expected: ['A', 'B', 'C', 'D', 'E', 'F'] or similar order based on neighbor iteration

    # Example 2: Disconnected Graph (BFS will only explore the connected component)
    graph2 = {
        '1': ['2', '3'],
        '2': ['1', '4'],
        '3': ['1', '5'],
        '4': ['2'],
        '5': ['3'],
        '6': ['7'],
        '7': ['6']
    }
    print("\nBFS Traversal for Graph 2 (starting from '1'):")
    print(bfs(graph2, '1')) # Expected: ['1', '2', '3', '4', '5'] or similar

    # Example 3: Graph with a single node
    graph3 = {
        'X': []
    }
    print("\nBFS Traversal for Graph 3 (starting from 'X'):")
    print(bfs(graph3, 'X')) # Expected: ['X']

    # Example 4: Empty graph (will raise an error if start_node is not in graph)
    graph4 = {}
    try:
        print("\nBFS Traversal for Graph 4 (starting from 'Z'):")
        print(bfs(graph4, 'Z'))
    except ValueError as e:
        print(e)