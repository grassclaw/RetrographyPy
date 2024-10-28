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

# Base Class: Operations
class Operation:
    def __init__(self, numbers):
        self.numbers = numbers

    def execute(self):
        raise NotImplementedError("This method should be overridden by subclasses")

# Subclass: addition
class Addition(Operation):
    def execute(self):
        return sum(self.numbers)

# Subclass: subtraction
class Subtraction(Operation):
    def execute(self):
        result = self.numbers[0]
        for num in self.numbers[1:]:
            result -= num
        return result

# Subclass: multiplication
class Multiplication(Operation):
    def execute(self):
        result = 1
        for num in self.numbers:
            result *= num
        return result

# Subclass: division
class Division(Operation):
    def execute(self):
        result = self.numbers[0]
        for num in self.numbers[1:]:
            if num == 0:
                raise ZeroDivisionError("Cannot divide by zero.")
            result /= num
        return result

# Subclass: Exponentiation
class Exponentiation(Operation):
    def execute(self):
        result = self.numbers[0]
        print(result)
        for num in self.numbers[1:]:
            result **= num
        return result

# Base Class: Calc Manager
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
    # Custom Type Conversion Function: Validate and convert the number arguments
    @staticmethod #took me a while to figure out why I needed to put this line
    def convert_to_float(value):
        try:
            return float(value)
        except ValueError:
            skipped_args.append(value)  # This modifies the global variable
            return None # skip non-numerics
    @staticmethod
    def get_user_input(prompt, type_=str):
        while True:
            try:
                value = type_(input(prompt))
                return value
            except ValueError:
                print("Invalid input. Please try again.")
  
# Custom: exception for invalid operations
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
def main():
    calculator = Calculator()
    # Set up argument parsing
    # Per the documentation, you can simply just tell argparse not to do anything for errors.
    # However, you definitely want to make sure you catch the error's elsewhere.
    parser = argparse.ArgumentParser(description="A Command-line calculator.")
    parser.add_argument("operation", help="The operation to perform (add, sub, mul, div, pow)")
    parser.add_argument("numbers", nargs='+', type=calculator.convert_to_float, help="Numbers for operation")

    args = parser.parse_args()
    
    while len(args.numbers) < 2:
        args.numbers = calculator.get_user_input("Please enter at least 2 #'s with a space in between: ")

    # I get none vals because I want to take args even if invalids are present
    args.numbers = [num for num in args.numbers if num is not None]

    print("Operation:", args.operation)
    print("Valid Numbers:", args.numbers)
    print("Skipped arguments (invalid):", skipped_args)

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
