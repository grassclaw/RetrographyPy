import sys

# Error handling per the instructions of the assignment. I have the program exit on error this time.
# Note:
#   - it wasn't necessary to use a list since python treats strings as a slice (javascript too, etc.). 
#   However, for the instructions, I used a list anyways.
class InvalidOperationError(Exception):
    pass

def main():
    if len(sys.argv) != 5:
        # As provided int he class instructions
        print("Please use this format: python convert.py <input_file> <output_file> <starting_offset (numeric)> <max_chars_to_convert(numeric)>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        starting_offset = int(sys.argv[3])
        max_chars_to_convert = int(sys.argv[4])
    except ValueError:
        print("Error: starting_offset and max_chars_to_convert must be numeric. (e.g. 4 19)")
        sys.exit(1)

    try:
        with open(input_file, 'r') as infile:
            data = infile.read()
    except FileNotFoundError:
        print(f"Error: Unable to open/find input file '{input_file}'.")
        sys.exit(1)

    try:
        outfile = open(output_file, 'w')
    except IOError:
        print(f"Error: Unable to open/find output file '{output_file}'.")
        sys.exit(1)

    length = len(data)
    midpoint = length // 2

    # Check for out-of-bounds starting_offset
    if starting_offset < 0 or starting_offset >= length:
        print(f"Error: starting_offset ({starting_offset}) is out of bounds.")
        print(f"The file contains {length} bytes. Please choose a starting_offset between 0 and {length - 1}.")
        sys.exit(1)

    # Check for invalid max_chars_to_convert
    if max_chars_to_convert <= 0:
        print("Error: max_chars_to_convert must be a positive integer.")
        sys.exit(1)

    # Determine start_index (use midpoint logic for positive/negative indexing)
    if starting_offset <= midpoint:
        start_index = starting_offset
    else:
        start_index = -(length - starting_offset)

    # Ensure the slice doesn't exceed the file size
    end_index = min(start_index + max_chars_to_convert, length)
    segment = data[start_index:end_index]

    # Convert the segment to uppercase
    modified_segment = segment.upper()

    # Combine the unchanged and modified parts
    output_data = data[:start_index] + modified_segment + data[end_index:]

    # Write to the output file
    with outfile:
        outfile.write(output_data)

    print(f"Conversion successful. Output written to '{output_file}'.")

if __name__ == "__main__":
    main()
