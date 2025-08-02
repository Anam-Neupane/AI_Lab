import heapq

def a_star(graph, start_node, goal_node, heuristic):
    """
    Performs A* Search on a graph.

    Args:
        graph (dict): Dictionary where keys are nodes and values are lists of (neighbor, cost) tuples.
        start_node: The node to start the search from.
        goal_node: The goal node to reach.
        heuristic (function): A function h(n) that estimates the cost from node n to the goal.

    Returns:
        list: The path from start_node to goal_node, or an empty list if no path is found.
    """
    if start_node not in graph or goal_node not in graph:
        raise ValueError("Start or goal node not found in the graph.")

    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start_node), 0, start_node, [start_node]))  # (f, g, node, path)
    visited = {}

    while open_set:
        f, g, current_node, path = heapq.heappop(open_set)

        if current_node == goal_node:
            return path

        if current_node in visited and visited[current_node] <= g:
            continue
        visited[current_node] = g

        for neighbor, cost in graph.get(current_node, []):
            new_g = g + cost
            new_f = new_g + heuristic(neighbor)
            heapq.heappush(open_set, (new_f, new_g, neighbor, path + [neighbor]))

    return []

# --- Example Usage ---

if __name__ == "__main__":
    # Example graph: Each node has neighbors with associated costs
    graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('D', 2), ('E', 5)],
        'C': [('A', 4), ('F', 3)],
        'D': [('B', 2)],
        'E': [('B', 5), ('F', 1)],
        'F': [('C', 3), ('E', 1)]
    }

    # Heuristic function (straight-line distances to goal 'F')
    def heuristic(n):
        h_values = {
            'A': 6,
            'B': 5,
            'C': 3,
            'D': 6,
            'E': 2,
            'F': 0
        }
        return h_values.get(n, float('inf'))

    print("A* Path from A to F:")
    path = a_star(graph, 'A', 'F', heuristic)
    print(" -> ".join(path))  # Expected path: A -> B -> E -> F or A -> C -> F (depending on heuristic)
