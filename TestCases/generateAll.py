from z3 import *
from itertools import permutations
import csv

def get_all_possible_values(number_of_variables, target_sum, output_file):
    # Create a Z3 solver
    solver = Solver()

    # Create Z3 variables for x1, x2, x3, and x4
    x = []
    for i in range(0, number_of_variables):
        var_name = f'x{i+1}'
        var = Int(var_name)
        solver.add(var > 0)
        x.append(var)

    # Adding constraint
    solver.add(Sum(x) == target_sum)

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        header = [f'x{i+1}' for i in range(number_of_variables)]
        writer.writerow(header)

        iter = 500

        # Iterate over all satisfying models
        while (solver.check() == sat) & (iter > 0):
            # Get the model
            iter = iter-1
            model = solver.model()

            values = [model.eval(var).as_long() for var in x]

            # write in CSV file
            writer.writerow(values)

            # Print the values dynamically based on the number of variables
            # variables_str = ', '.join(f'x{i+1} = {val}' for i, val in enumerate(values))
            # print(variables_str)

            # Add constraint to exclude the current solution and it's permutations
            allPermuations = list(permutations(values))
            for per in allPermuations:
                constraint = Or(*[var != val for var, val in zip(x, per)])
                solver.add(constraint)

# Get and print all possible values
def main():
    variables = int(input("Number of variables: "))
    total = int(input("Sum: "))
    fileName = input("File name: ")
    get_all_possible_values(variables, total, fileName)

# If the it is called from this function
if __name__ == "__main__":
    main()