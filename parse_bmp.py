#import Packages
import struct, sys, os

#Questions I had during program
#   Q: What is the normal for handling exceptions, errors, etc in python?
#   A: https://stackoverflow.com/questions/16138232/is-it-a-good-practice-to-use-try-except-else-in-python
#   Q: Do python programmers use camelcase or underscores?
#   A: https://peps.python.org/pep-0008/
#   Q: how to print bytes to a string?
#   A: https://stackoverflow.com/questions/606191/convert-bytes-to-a-string-in-python-3

# COMMENTS: Did a lot of research on what would indicate a file is not in proper BMP format
# Added error checking for improper BMP format. Needs further investigation.

#Func parse_header
def parse_header(f_path):
    try:
        with open(f_path, 'rb') as f:
            # Read the first 54 bytes of the BMP file
            header = f.read(30)
            #CHECK FILE TYPE
            if header[0:2] != b'BM':
                print("Not a BMP image file. Please check file type.")
                return False

            #PROCESS Decode
            print(f"BMP Header: {header[0:28].hex()}")
            # little endian - 
                #0# 2/2 byte - 2 string #FileType
                #1# 4/6 byte - I unsigned 32-bit int #File Size
                #2# 2/8 byte - H unsigned 16-bit int #Reserved 1
                #3# 2/10 byte - H #Reserved 2
                #4# 4/14 byte - I #DataOffset
                #5# 4/18 byte - I #HeaderSize
                #6# 4/22 byte - i signed 32-bit int #ImageWidth
                #7# 4/26 byte - i #ImageHeight <--This took me a little bit to realize what was going on and why i wanted signed
                #8# 2/28 byte - H #Planes
                #9# 2/30 byte - H #BitsPerPixel
            header_format = '<2sIHHIIiiHH' #Could do individually by line or all in one
            # Unpack the entire BMP header
            bmp_header = struct.unpack(header_format, header)
            # Print Desired Data
            print(f"File Type: {str(bmp_header[0],'utf-8')}")
            #Check for incorrect file size
            actual_size = os.path.getsize(f_path)#file size
            if bmp_header[1] != actual_size:
                print("Alert! File Size Mismatch: Header")
                return False
            print(f"File Size: {bmp_header[1]} bytes")
            print(f"Reserved1: {bmp_header[2]} bytes")
            print(f"Reserved2: {bmp_header[3]} bytes")
            # Ensures minimum offset for BMP file format
            if bmp_header[4]<54:
                print("Alert! Pixel Offset: Possible corrupted file: Header")
                return False
            print(f"Data/Pixel Offset: {bmp_header[4]} bytes")
            print(f"Header Size: {bmp_header[5]} bytes")
            print(f"Image Width: {bmp_header[6]} bytes")
            print(f"Image Height: {bmp_header[7]} bytes")
            # Color Pane NOT 1 is possibly corrupted and not BMP format
            if bmp_header[8]!= 1:
                print("Alert! Color Planes: Possible Malformed File: Header")
                return False
            print(f"Planes: {bmp_header[8]} bytes")
            if bmp_header[9] not in [1, 4, 8, 16, 24, 32]:
                print("Alert! Bits per Pixel: Possible File Corruption: Header")
                return False
            print(f"Bits per Pixel: {bmp_header[9]} bytes")
    # Apparently 'try' statements require at least on except
    #could be some others to add but not familiar with pythons error handling
    # Handle File Errors
    except FileNotFoundError:
        print(f"Error: '{f_path}' Not Found")
        return False
    return True

#MAIN
#Ingest argument/associated files
def main():
    # file path is not provided then abort and exit
    if len(sys.argv) < 2:
        print("No File Specified...Usage: python script_name.py <file_path1>...")
        sys.exit(1)

    # Iterate over all files
    for f_path in sys.argv[1:]:
        print('-' * 40)
        print(f"DECODE HEADER: {f_path}" )
        print(f"OPERATION SUCCESS: {parse_header(f_path)}")

if __name__ == "__main__":
    main()



# TROUBLESHOOTING PROMPTS USED - ARCHIVED

    # unsigned_value = bmp_header[7][2]| (bmp_header[7][1]<< 8) | (bmp_header[7][0] << 16)
    # print(unsigned_value)
    # print(len(header[22:25]))
    # print(f"Image Height: {int.from_bytes(unsigned_value,byteorder='little')} bytes")
    # print(f"Image Height: {header[22:26].hex()} bytes")
