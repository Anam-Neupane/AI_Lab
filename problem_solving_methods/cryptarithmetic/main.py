def solve_cryptarithmetic_backtrack(puzzle):
    import re

    # Clean up input
    puzzle = puzzle.replace(" ", "")
    left_side, result = puzzle.split('=')
    words = re.split(r'[\+\-]', left_side) + [result]

    # Extract unique letters
    letters = sorted(set(''.join(words)))
    if len(letters) > 10:
        print("Too many unique letters!")
        return None

    leading_letters = set(word[0] for word in words)

    # Precompute letter positions: each letter contributes to the total by its position
    def get_letter_weights(words, result):
        weights = {}
        for word in words[:-1]:
            for i, letter in enumerate(reversed(word)):
                weights[letter] = weights.get(letter, 0) + 10 ** i
        for i, letter in enumerate(reversed(result)):
            weights[letter] = weights.get(letter, 0) - 10 ** i
        return weights

    letter_weights = get_letter_weights(words, result)

    # Recursive backtracking function
    def backtrack(index, assignment, used_digits):
        if index == len(letters):
            # All letters assigned, check if total == 0
            total = sum(letter_weights[letter] * digit for letter, digit in assignment.items())
            if total == 0:
                return assignment
            return None

        letter = letters[index]
        for digit in range(10):
            if digit in used_digits:
                continue
            if letter in leading_letters and digit == 0:
                continue  # leading digit can't be zero

            # Assign digit
            assignment[letter] = digit
            used_digits.add(digit)

            result = backtrack(index + 1, assignment, used_digits)
            if result:
                return result

            # Backtrack
            del assignment[letter]
            used_digits.remove(digit)

        return None

    # Start backtracking
    return backtrack(0, {}, set())

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
            solution = solve_cryptarithmetic_backtrack(puzzle_str)
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
            continue
