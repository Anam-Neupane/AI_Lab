import pickle
import os

# Path to the saved Q-table
SAVE_PATH = "q_table3.pkl"

# Check if the file exists
if not os.path.exists(SAVE_PATH):
    print(f"File '{SAVE_PATH}' not found.")
else:
    # Load the Q-table
    with open(SAVE_PATH, "rb") as f:
        q_table = pickle.load(f)

    print(f"Total States Learned: {len(q_table)}\n")

    # Print a few entries from the Q-table for inspection
    for i, (state, values) in enumerate(q_table.items()):
        print(f"State {i+1}: {state} => Q-values: {values}")
        if i >= 9:  # Print only first 10 states to keep it readable
            break

    # Optional: Inspect specific state
    sample_state = (1, 0, 1)  # Example state (dx, dy, direction_code)
    if sample_state in q_table:
        print(f"\nSample State {sample_state} has Q-values: {q_table[sample_state]}")
    else:
        print(f"\nSample State {sample_state} not found in Q-table.")
