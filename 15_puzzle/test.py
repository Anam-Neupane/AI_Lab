import model

puzzle = model.Puzzle()
print("Initial Puzzle State:")
print(puzzle)
print("Solved?", puzzle.checkWin())
input("Press Enter to continue...")

puzzle.shuffle()
print("Shuffled Puzzle State:")
print(puzzle)
print("Solved?", puzzle.checkWin())
input("Press Enter to continue...")

print("Blank Position:", puzzle.blankPos)
print("Moving blank square UP:")
puzzle.move(model.Puzzle.UP)
print(puzzle)
input("Press Enter to continue...")

print("Blank Position after move:", puzzle.blankPos)
print("Moving blank square LEFT:")
puzzle.move(model.Puzzle.LEFT)
print(puzzle)
input("Press Enter to continue...")

print("Blank Position after move:", puzzle.blankPos)
print("Moving blank square DOWN:")
puzzle.move(model.Puzzle.DOWN)
print(puzzle)
input("Press Enter to continue...")

print("Blank Position after move:", puzzle.blankPos)
print("Moving blank square RIGHT:")
puzzle.move(model.Puzzle.RIGHT)
print(puzzle)
input("Press Enter to continue...")

puzzle.move(model.Puzzle.RIGHT)
puzzle.move(model.Puzzle.RIGHT)
puzzle.move(model.Puzzle.RIGHT)
puzzle.move(model.Puzzle.RIGHT)
# Attempting to move out of bounds
print("Attempting to move out of bounds (RIGHT):")
print(puzzle)
input("Press Enter to continue...")

puzzle3 = model.Puzzle(3)
print("3x3 Puzzle State:")
print(puzzle3)


