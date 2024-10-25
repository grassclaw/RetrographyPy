import argparse
import sys
# List to store skipped (invalid) arguments
skipped_args = []
# Custom exception for invalid operations
class InvalidOperationError(Exception):
    def __init__(self, message):
        super().__init__(message)

# Define the functions for each operation
def add(numbers):
    return sum(numbers)

def sub(numbers):
    result = numbers[0]
    for num in numbers[1:]:
        result -= num
    return result

def mul(numbers):
    result = 1
    for num in numbers:
        result *= num
    return result

def div(numbers):
    result = numbers[0]
    for num in numbers[1:]:
        if num == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        result /= num
    return result

def power(numbers):
    result = numbers[0]
    for num in numbers[1:]:
        result **= num
    return result

# Define the main calculator function
def calculator(operation, numbers):
    operations = {
        "add": add,
        "sub": sub,
        "mul": mul,
        "div": div,
        "pow": power
    }
    
    if operation not in operations:
        raise InvalidOperationError(f"Unsupported operation. Please choose from: {', '.join(operations.keys())}")
    
    # Get the function based on the operation and execute it with the numbers
    return operations[operation](numbers)

# Helper function to validate and convert the number arguments
def convert_to_float(number_str):
    try:
        return float(number_str)
    except ValueError:
        skipped_args.append(number_str)  # Add invalid inputs to the skipped list
        return None

# Custom argparse error handler class
class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        # Override the default error behavior to prevent SystemExit
        sys.stderr.write(f"Error: {message}\n")
        sys.exit(2)  # Optionally, you can use any custom exit code here or return gracefully

def main():
    # Use the custom argument parser to handle errors
    # parser = CustomArgumentParser(prog="Python Calculator", description="A command-line calculator.")
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", help="The operation to perform (add, sub, mul, div, pow)")
    parser.add_argument("numbers", nargs='+', type=convert_to_float, help="Numbers on which to perform the operation")
    args = parser.parse_args()

    # Filter out any None values (non-numeric inputs)
    filtered_numbers = [num for num in args.numbers if num is not None]

    print("Operation:", args.operation)
    print("Valid Numbers:", filtered_numbers)
    print("Skipped arguments (invalid):", skipped_args)

    # try:
    #     # Attempt to parse the arguments
    #     args = parser.parse_args()

    #     # Ensure there are at least two numbers
    #     if len(args.numbers) < 2:
    #         print("Error: You must provide at least two numbers.")
    #         return
    #     try:
    #         result = calculator(args.operation, args.numbers)
    #         print(f"Result: {result}")
    #     except InvalidOperationError as e:
    #         print(f"Error: {e}")
    #     except ZeroDivisionError as e:
    #         print(f"Error: {e}")
    #     except Exception as e:
    #         print(f"An unexpected error occurred: {e}")
    # except SystemExit as e:
    #     if e.code != 0:
    #         print("An error occurred while parsing the arguments. Please check your input.")

if __name__ == "__main__":
    main()
