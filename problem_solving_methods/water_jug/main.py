from collections import deque

def water_jug_bfs(jug1_capacity, jug2_capacity, target):

    visited = set()
    queue = deque()
    parent = dict()  # For backtracking the path

    start = (0, 0)
    queue.append(start)
    parent[start] = None  # Start has no parent

    while queue:
        jug1, jug2 = queue.popleft()
# or jug2 == target or jug1 + jug2 == target
        # Check if target is found in either jug or their sum
        if jug1 == target :
            final_state = (jug1, jug2)
            # 🔁 Backtrack the path
            path = []
            while final_state:
                path.append(final_state)
                final_state = parent[final_state]
            path.reverse()

            # Print the path
            print(f"Target {target} can be reached with the following path:")
            for state in path:
                print(state)
            return True

        if (jug1, jug2) in visited:
            continue
        visited.add((jug1, jug2))

        # All possible next states
        possible_states = [            

            (jug1_capacity, jug2),  # Fill jug1
            (jug1, jug2_capacity),  # Fill jug2
            (0, jug2),              # Empty jug1
            (jug1, 0),              # Empty jug2
            # Pour jug1 → jug2
            (jug1 - min(jug1, jug2_capacity - jug2), jug2 + min(jug1, jug2_capacity - jug2)),
            # Pour jug2 → jug1
            (jug1 + min(jug2, jug1_capacity - jug1), jug2 - min(jug2, jug1_capacity - jug1))
        ]

        for state in possible_states:
            # print("State 1"+ str(state))
            if state not in visited and state not in parent:
                queue.append(state)
                # print("Visited"+ str(state))
                parent[state] = (jug1, jug2)

    print(f"Target {target} cannot be reached.")
    return False

# Example usage
jug1_capacity = int(input("Enter the capacity of jug 1: "))
jug2_capacity = int(input("Enter the capacity of jug2: "))
target = int(input("Enter the target litre you want to achieve: "))  # Change this to 1 to see path to (1, 0)
print(f"jug1={jug1_capacity}, jug2={jug2_capacity} and traget={target}")
water_jug_bfs(jug1_capacity, jug2_capacity, target)
