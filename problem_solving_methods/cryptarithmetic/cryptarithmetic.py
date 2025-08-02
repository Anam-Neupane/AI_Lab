def solve_cryptarithmetic(puzzle):
    """
    Solves a cryptarithmetic puzzle.

    Args:
        puzzle (str): The cryptarithmetic puzzle as a string, e.g., "SEND + MORE = MONEY".

    Returns:
        dict or None: A dictionary mapping letters to digits if a solution is found,
                      otherwise None.
    """
    
    parts = puzzle.replace(" ", "").split("=")
    if len(parts) != 2:
        raise ValueError("Invalid puzzle format. Expected 'EXPRESSION = RESULT'.")
    
    expression = parts[0]
    result = parts[1]

    # Extract unique letters
    letters = sorted(list(set(c for c in expression + result if 'A' <= c <= 'Z')))
    if len(letters) > 10:
        print("Error: More than 10 unique letters. Cryptarithmetic puzzles typically use 0-9.")
        return None

    # Get the words involved
    words = []
    
    # Process the expression part
    if '+' in expression:
        words.extend(expression.split('+'))
    elif '-' in expression:
        words.extend(expression.split('-'))
    elif '*' in expression:
        words.extend(expression.split('*'))
    elif '/' in expression:
        words.extend(expression.split('/'))
    else:
        words.append(expression) # Single word on the left if no operator
        
    words.append(result)

    # Identify leading letters (cannot be zero)
    leading_letters = set()
    for word in words:
        if word:  # Ensure the word is not empty
            leading_letters.add(word[0])

    # Generate permutations of digits for the letters
    import itertools

    for perm in itertools.permutations(range(10), len(letters)):
        mapping = {letters[i]: perm[i] for i in range(len(letters))}

        # Check leading zeros
        if any(mapping[l] == 0 for l in leading_letters):
            continue

        # Evaluate the expression
        try:
            # Create a string where letters are replaced by their mapped digits
            # For evaluation, we need to reconstruct the numerical expression
            
            # Replace letters in words with digits to form numbers
            num_words = []
            for word in words:
                num_word = int("".join(str(mapping[char]) for char in word))
                num_words.append(num_word)

            # Reconstruct the numerical equation for evaluation
            # This handles different operators
            
            eval_expression = ""
            current_index = 0
            
            # Iterate through the original expression to find operators and combine numbers
            for char in expression:
                if char in "+-*/":
                    eval_expression += char
                elif 'A' <= char <= 'Z':
                    if current_index < len(words) -1 and words[current_index].startswith(char):
                        eval_expression += str(num_words[current_index])
                        current_index += 1
            
            # Add the last number on the left side
            if current_index < len(words) -1: # check to make sure words isn't exhausted
                eval_expression += str(num_words[current_index])
            
            # The result part is always the last word in num_words
            eval_result = num_words[-1]

            # Evaluate the left side of the equation
            if eval(eval_expression) == eval_result:
                return mapping
        except (ValueError, SyntaxError):
            # This can happen if eval_expression is malformed or if numbers become too large
            continue
    return None

# --- Examples ---

if __name__ == "__main__":
    puzzles = [
        "SEND + MORE = MONEY",
        "TOO + TOO = FOUR",
        "CROSS + ROADS = DANGER",
        "SIX - TWO = FOUR", # Example with subtraction
        "ODD + ODD = EVEN",
        "EAT + THAT = APPLE",
        "BASE + BALL = GAMES",
        "HAPPY + SAD = GOOD",
        "FIFTY + FIFTY = HUNDRED",
        "USA + USSR = PEACE",
        "SATURN + URANUS = PLANETS",
        "I + AM = MAN",
        "A + B = C",
        "GO + GO = OUT",
        "COCA + COLA = OASIS", # Example where no solution might be obvious
        "FUN + FUN = FUNNY",
        "EARTH + WIND = FIRE",
        "DONALD + GERALD = ROBERT",
        "ABC * DE = FGH", # Multiplication example (simplified as single word on left for demo)
        "HELLO / BYE = HI" # Division example (simplified as single word on left for demo)
    ]

    for puzzle_str in puzzles:
        print(f"\nSolving: {puzzle_str}")
        try:
            solution = solve_cryptarithmetic(puzzle_str)
            if solution:
                print("Solution found:")
                for letter, digit in sorted(solution.items()):
                    print(f"  {letter} = {digit}")

                # Verify the solution
                # Replace letters in the original puzzle string with digits
                solved_puzzle = puzzle_str
                for letter, digit in solution.items():
                    solved_puzzle = solved_puzzle.replace(letter, str(digit))
                print(f"Verification: {solved_puzzle}")

            else:
                print("No solution found.")
        except ValueError as e:
            print(f"Error: {e}")
        
