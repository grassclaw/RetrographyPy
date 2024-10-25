import argparse

# INSPIRATION:
# https://stackoverflow.com/questions/42249982/systemexit-2-error-when-calling-parse-args-within-ipython
# https://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
# https://docs.python.org/3/library/argparse.html

# ERROR Handling:
# I use a custom convert to float to capture invalid arguments in this case.
# This also prevent command line injection as seen in the following example (use of *):
        # python3 calculator.py add 1.1 2.4 t asdf  *
        # Operation: add
        # Valid Numbers: [1.1, 2.4]
        # Skipped arguments (invalid): ['t', 'asdf', 'calculator copy.py', 'calculator.py', 'class_ex', 'mexsync', 'parse_bmp.py', 'polymorph_example.py']
        # Result: 3.5

# GLOBAL VARIABLS
# I usually frown on global variables but this is more for info purposes
skipped_args = []  # This captures invalid arguments

# Base class for all operations
class Operation:
    def __init__(self, numbers):
        self.numbers = numbers

    def execute(self):
        raise NotImplementedError("This method should be overridden by subclasses")

# Subclass for addition
class Addition(Operation):
    def execute(self):
        return sum(self.numbers)

# Subclass for subtraction
class Subtraction(Operation):
    def execute(self):
        result = self.numbers[0]
        for num in self.numbers[1:]:
            result -= num
        return result

# Subclass for multiplication
class Multiplication(Operation):
    def execute(self):
        result = 1
        for num in self.numbers:
            result *= num
        return result

# Subclass for division
class Division(Operation):
    def execute(self):
        result = self.numbers[0]
        for num in self.numbers[1:]:
            if num == 0:
                raise ZeroDivisionError("Cannot divide by zero.")
            result /= num
        return result

# Subclass for exponentiation
class Exponentiation(Operation):
    def execute(self):
        result = self.numbers[0]
        for num in self.numbers[1:]:
            result **= num
        return result

# Calculator class that manages operation delegation
class Calculator:
    def __init__(self):
        # Map operation names to corresponding classes
        self.operations = {
            "add": Addition,
            "sub": Subtraction,
            "mul": Multiplication,
            "div": Division,
            "pow": Exponentiation
        }

    def perform_operation(self, operation_name, numbers):
        if operation_name not in self.operations:
            raise InvalidOperationError(f"Unsupported operation. Please choose from: {', '.join(self.operations.keys())}")
        
        # Instantiate the appropriate operation class and execute
        operation_class = self.operations[operation_name](numbers)
        return operation_class.execute()

# Custom exception for invalid operations
class InvalidOperationError(Exception):
    def __init__(self, message):
        super().__init__(message)

def convert_to_float(value):
    try:
        return float(value)
    except ValueError:
        skipped_args.append(value)  # This modifies the global variable
        return None

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="A simple command-line calculator with class-based operations.")
    parser.add_argument("operation", help="The operation to perform (add, sub, mul, div, pow)")
    parser.add_argument("numbers", nargs='+', type=convert_to_float, help="Numbers on which to perform the operation")

    args = parser.parse_args()

    # Ensure there are at least two numbers
    if len(args.numbers) < 2:
        print("Error: You must provide at least two numbers.")
        return
    args.numbers = [num for num in args.numbers if num is not None]

    print("Operation:", args.operation)
    print("Valid Numbers:", args.numbers)
    print("Skipped arguments (invalid):", skipped_args)

    # Create a Calculator instance
    calculator = Calculator()

    try:
        result = calculator.perform_operation(args.operation, args.numbers)
        print(f"Result: {result}")
    except InvalidOperationError as e:
        print(f"Error: {e}")
    except ZeroDivisionError as e:
        print(f"Error: {e}")
    except ValueError:
        print("Error: Both arguments must be numbers.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
