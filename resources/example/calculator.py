import argparse

# INSPIRATION:
# https://stackoverflow.com/questions/42249982/systemexit-2-error-when-calling-parse-args-within-ipython
# https://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
# https://docs.python.org/3/library/argparse.html

# ERROR Handling:
# I use a custom convert to float to capture invalid arguments in this case.
# This also prevent command line injection as seen in the following example (use of *):
# % python3 resources/example/calculator.py mod 2 *            
#       Invalid or missing operation. Please enter one of: add, sub, mul, div, pow
#       Enter operation (add, sub, mul, div, pow): pow
#       Error: You must provide at least two valid numbers.      
#       Enter numbers separated by spaces: 2 2 *
#       Operation: pow
#       Valid Numbers: [2.0, 2.0]
#       Skipped arguments (invalid): ['LICENSE', 'README.md', 'resources', '*']
#       Result: 4.0

# GLOBAL VARIABLS
# I usually frown on global variables but this is more for info purposes
skipped_args = []

# Base Class: Operations
class Operation:
    def __init__(self, numbers):
        self.numbers = numbers

    def execute(self):
        raise NotImplementedError("This method should be overridden by subclasses")

# The following methods for the operations were found on the internet. 
# I created my own but looked more forgiving/effecient methods

# Subclass: addition (add)
class Addition(Operation):
    def execute(self):
        return sum(self.numbers)

# Subclass: subtraction (sub)
class Subtraction(Operation):
    def execute(self):
        result = self.numbers[0]
        for num in self.numbers[1:]:
            result -= num
        return result

# Subclass: multiplication (mul)
class Multiplication(Operation):
    def execute(self):
        result = 1
        for num in self.numbers:
            result *= num
        return result

# Subclass: division (div)
class Division(Operation):
    def execute(self):
        result = self.numbers[0]
        for num in self.numbers[1:]:
            if num == 0:
                raise ZeroDivisionError("Cannot divide by zero.")
            result /= num
        return result

# Subclass: Exponentiation (pow)
class Exponentiation(Operation):
    def execute(self):
        result = self.numbers[0]
        for num in self.numbers[1:]:
            result **= num
        return result

# Calculator Manager Class
class Calculator:
    def __init__(self):
        # Op names to corresponding classes
        self.operations = {
            "add": Addition,
            "sub": Subtraction,
            "mul": Multiplication,
            "div": Division,
            "pow": Exponentiation
        }

    def perform_operation(self, operation_name, numbers):
        # We check appropriate op in input def. We execute here.
        operation_class = self.operations[operation_name](numbers)
        return operation_class.execute()

    # Custom Type Conversion Function: Validate and convert the number arguments
    @staticmethod #took me a while to figure out why I needed to put this line
    def convert_to_float(value):
        try:
            return float(value)
        except ValueError:
            skipped_args.append(value) # This modifies the global variable
            return None  # Skip non-numeric arguments

# Custom exception for invalid operations
class InvalidOperationError(Exception):
    def __init__(self, message):
        super().__init__(message)

# Custom: argparse error handler 
# I moved away from this. I decided it was cleaner through the custom float instead.
# The logic here was to overwrite Argparse default error handling which results
# in exit which in my opinion isn't the best handling for a robust app
# class CustomArgumentParser(argparse.ArgumentParser):
    # def error(self, message):
        # Override the default error behavior to prevent SystemExit
        # sys.stderr.write(f"Error: {message}\n")
        # sys.exit(2)  # Optionally, you can use any custom exit code here or return gracefully
# Function to parse arguments initially from command-line or re-prompt

def parse_arguments():
    parser = argparse.ArgumentParser(description="A Command-line calculator.")
    parser.add_argument("operation", help="The operation to perform (add, sub, mul, div, pow)")
    parser.add_argument("numbers", nargs='*', help="Numbers for operation")
    
    try:
        args = parser.parse_args()
        return args.operation, args.numbers
    except SystemExit:
        return None, None

# Function to validate and re-prompt if necessary
def get_valid_input(calculator):
    while True:
        # Initial argument parsing from command-line
        operation, numbers_input = parse_arguments()

    # THIS seems like an incredibly wasteful way to check but I wanted a robust method to reprompt users for a variety of usr mistakes
    # There's definitely space to create yet another subclass or def to reinstitue numbers list
    # Just short of spending too much time cleaning this code, it was the best I came up with after a few versions
        # CHECK: Invalid Op
        while operation not in calculator.operations:
            print("Invalid or missing operation. Please enter one of: add, sub, mul, div, pow")
            operation = input("Enter operation (add, sub, mul, div, pow): ").strip()
        
        # CHECK: more than 1 #...handles/skips invalid inputs
        numbers = []
        while len(numbers) < 2:
            # Convert to float and skip non-numerics which are stored in skip array
            numbers = [calculator.convert_to_float(num) for num in numbers_input or []]
            numbers = [num for num in numbers if num is not None]
            if len(numbers) < 2:
                print("Error: You must provide at least two valid numbers.")
                numbers_input = input("Enter numbers separated by spaces: ").strip().split()
        
        # CHECK: Divide by 0
        while operation == "div" and 0 in numbers[1:]:
            numbers = [calculator.convert_to_float(num) for num in numbers_input or []]
            numbers = [num for num in numbers if num is not None]
            if operation == "div" and 0 in numbers[1:]:
                print("Error: Division by zero detected. Please enter numbers that do not include zero in the divisor.")
                numbers_input = input("Enter numbers separated by spaces (excluding zero for divisor): ").strip().split()
                        
        return operation, numbers

def main():
    calculator = Calculator()

    # Get valid input and perform calculation
    operation, numbers = get_valid_input(calculator)
    # Print Input Stats of Interest
    print("Operation:", operation)
    print("Valid Numbers:", numbers)
    print("Skipped arguments (invalid):", skipped_args)

    try:
        result = calculator.perform_operation(operation, numbers)
        print(f"Result: {result}")
    except InvalidOperationError as e:
        print(f"Error: {e}. Please enter a valid operation.")
    except ZeroDivisionError as e:
        print(f"Error: {e}. Please enter a new set of numbers that do not include zero in the divisor.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
