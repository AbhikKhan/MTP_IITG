from z3 import *
from itertools import permutations

def get_all_possible_values(target_sum):
    # Create Z3 variables for x1, x2, x3, and x4
    x1 = Int('x1')
    x2 = Int('x2')
    x3 = Int('x3')
    x4 = Int('x4')

    # Create a Z3 solver
    solver = Solver()

    # Add constraints to the solver
    solver.add(x1 > 0)
    solver.add(x2 > 0)
    solver.add(x3 > 0)
    solver.add(x4 > 0)
    solver.add(x1 + x2 + x3 + x4 == target_sum)

    # Iterate over all satisfying models
    while solver.check() == sat:
        # Get the model
        model = solver.model()

        values = [model.eval(var).as_long() for var in [x1, x2, x3, x4]]

        print(f"x1 = {values[0]}, x2 = {values[1]}, x3 = {values[2]}, x4 = {values[3]}")

        # Add constraint to exclude the current solution
        allPermuations = list(permutations(values))
        for per in allPermuations:
            solver.add(Or(x1 != per[0], x2 != per[1], x3 != per[2], x4 != per[3]))

# Get and print all possible values
def main():
    total = input("Sum: ")
    get_all_possible_values(total)

# If the it is called from this function
if __name__ == "__main__":
    main()