#Retrography


Objective:
Write a Python program that reads a BMP (bitmap) file and parses its header to extract key
information. This exercise will reinforce your understanding of binary data handling in Python,
as well as give you insight into how file formats are structured—a critical skill in cybersecurity
and cover channels.
Requirements:
You will need to manually parse the file header without using any libraries that perform this task
for you (e.g., PIL, imageio). You are allowed to use Python’s built-in libraries like struct for
unpacking binary data.
Tasks:
1. File Handling:
- Write a Python script that opens a BMP file in binary mode.
- Read the first 54 bytes of the file, which constitute the BMP header.
2. Header Parsing:
-Extract and print the following information from the BMP header:
File Type: The first 2 bytes should always be 'BM' for a bitmap file.
File Size: The size of the BMP file in bytes (bytes 2-5).
Reserved Fields: 4 bytes (bytes 6-9), typically set to 0.
Data Offset: The starting address of the bitmap data (bytes 10-13).
Header Size: The size of the header (should be 40 bytes for the
BITMAPINFOHEADER) (bytes 14-17).
Image Width: The width of the image in pixels (bytes 18-21).
Image Height: The height of the image in pixels (bytes 22-25).
Planes: The number of color planes being used. This is always 1 (bytes
26-27).
Bits per Pixel: The number of bits per pixel, which is the color depth of
the image (bytes 28-29).
3. Output:
Print the extracted information in a human-readable format.
4. Error Handling:
Ensure that your program gracefully handles errors, such as trying to read a non-
BMP file, files with incorrect sizes, or files that do not conform to the BMP
format.
Example Output: When your program is run with a BMP file, it should output something
similar to the following example:
File Type: BM
File Size: 1024 bytes
Reserved 1: 0
Reserved 2: 0
Data Offset: 54 bytes
Header Size: 40 bytes
Image Width: 100 pixels
Image Height: 100 pixels
Planes: 1
Bits per Pixel: 24
Submission:
Submit to D2L a single Python file named parse_bmp.py that contains your solution.