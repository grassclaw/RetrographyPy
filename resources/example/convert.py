import sys
# Error handling per the instructions of the assignment. I have the program exit on error this time.
# I just wend down the list for error handling this time.
# Note:
#   - it wasn't necessary to use a list since python treats strings as a slice (javascript too, etc.). 
#   However, for the instructions, I used a list anyways.


# I actually couldn't find a use for a custom invalid operation error. All the other requirements really cover the bases. 
# It seemed like this direction may have carried over from something like the calulator assignment.
class InvalidOperationError(Exception):
    pass

def main():
    # Just a simple, there's too many args here message
    if len(sys.argv) != 5:
        print("Please use this format: python convert.py <input_file> <output_file> <starting_offset (numeric)> <max_chars_to_convert(numeric)>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # First 3 args are the script, input, output file (0-2)
    try:
        starting_offset = int(sys.argv[3])
        max_chars_to_convert = int(sys.argv[4])
    except ValueError:
        # The int conversion will capture any non-numeric issues. A lot cleaner than my custom float handling from the calculator py
        print("Error: starting_offset and max_chars_to_convert must be numeric.")
        sys.exit(1)

    # Detect and swap if needed (e.g. b<a). I threw this in here for extra error check robustness
    if starting_offset > max_chars_to_convert:
        print(f"Swap initiated! starting_offset ({starting_offset}) is larger than max_chars_to_convert ({max_chars_to_convert}).")
        starting_offset, max_chars_to_convert = max_chars_to_convert, starting_offset

    # Really could just read into a string which is faster I believe. Python like many languages can iterate stringlike slicing.
    try:
        with open(input_file, 'r') as infile:
            # Read the file into a list of characters
            data = list(infile.read())
    except FileNotFoundError:
        print(f"Error: Unable to open input file '{input_file}'.")
        sys.exit(1)

    # Check for issues with output file which would be rare since it will create an output if none exist.
    try:
        outfile = open(output_file, 'w')
    except IOError:
        print(f"Error: Unable to open output file '{output_file}'.")
        sys.exit(1)

    # Per assignment instructions, find midpoint
    length = len(data)
    midpoint = length // 2

    # Check for out-of-bounds starting_offset
    if starting_offset < 0 or starting_offset >= length:
        print(f"Error: starting_offset ({starting_offset}) is out of bounds.")
        # I added this so the user can know what the bounds are even though they have to guess on the first try.
        # I considered deviating from the assignment instructions to first tell the user the bounds and then prompt for offsets
        print(f"The file contains {length} bytes. Please choose a starting_offset between 0 and {length - 1}.")
        sys.exit(1)

    # NOTE: This doesn't get triggered since i already check if it is in bounds...but per the instructions.>>
    # Check for invalid max_chars_to_convert
    if max_chars_to_convert <= 0 or starting_offset<=0:
        print("Error: max_chars_to_convert must be a positive integer.")
        sys.exit(1)

    
    # Determine start_index (use midpoint logic for positive or negative indexing)
    #   First Half: If the starting_offset is less than or equal to half of the total
    #       length of the data, you will use a positive index for slicing.
    #   Second Half: If the starting_offset is greater than half of the total length
    #       of the data, you will convert the positive starting_offset to a negative
    #       index for slicing.
    if starting_offset <= midpoint: 
        start_index = starting_offset
    else:
        start_index = -(length - starting_offset)

    # Ensure the slice doesn't exceed the file size
    end_index = min(start_index + max_chars_to_convert, length)
    segment = data[start_index:end_index]

    # Convert the segment to uppercase and track capitalized characters
    modified_segment = []
    transformed_segment = []
    for char in segment:
        upper_char = char.upper()
        transformed_segment.append(upper_char)  # Track every character, including spaces
        modified_segment.append(upper_char)


    # Combine the unchanged and modified parts
    output_data = data[:start_index] + modified_segment + data[end_index:]

    # Write to the output file as a string
    with outfile:
        outfile.write(''.join(output_data))

    print(f"Success! Output written to '{output_file}'.")
    print("Capitalized Letters:", ''.join(transformed_segment))


if __name__ == "__main__":
    main()
