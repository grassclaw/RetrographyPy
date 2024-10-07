import os,sys

# In this I demonstrate a couple ways to handle initializing instances of subclass. 
# I prefer the way the text is being handled 
# but to demonstrate overriding base class methods and attributes,
# I modified the image sub class.
# I also set the script for testing rather than assumed export of main

# Made this for File Base Class attribute filesize
def get_fsize(filename):
    try:
        # Get the file size in bytes
        file_size = os.stat(filename).st_size
        return file_size
    except FileNotFoundError:
        return "File not found."

# Base Class
class File:
    # Attributes of Base
    def __init__(self, filename):
        self.filename = filename
        self.filesize = get_fsize(filename) # calls file size function or passes error

    def open(self):
        # I liked this instead of pass. Adds a little extra information with errors
        raise NotImplementedError("Subclass requires open method. Missing.")
    
    def read(self):
        raise NotImplementedError("Subclasses requires read method. Missing.")
    
    # Base Class specific method
    def stats(self):
        print(f"File size: {self.filesize} bytes")

    
# Derived Class for Text Files
class TextProcessor(File):
    # All inheritance
    def open(self):
        # Simulate opening a text file
        print(f"Opening text file: {self.filename}")
        # Here you would add code to read the text file contents
    def read(self):
        try:
            # Simulate reading a text file
            with open(self.filename, 'r') as file:
                content = file.read()
                print(f"Reading text file: {self.filename}")
                print(content)
        except FileNotFoundError:
            print(f"Error: '{self.filename}' Not Found")
# Derived Class for Image Files
class ImageProcessor(File):
    def __init__(self, file_name, new_name):
        # I'm giving this image an identity crisis and ignoring the correct file name
        self.filename = new_name
        self.truename = file_name
    def open(self):
        # Simulate opening an image file
        print(f"Opening image file: {self.filename}")
        # Here you would add code to process the image file
    def read(self):
        # Simulate processing an image file
        print(f"Reading image file...: My actual name is {self.truename}. You found me!")
        # Could add code to manipulate the image. Probably would create another set of children class from here (bmp, png, etc.)
    # EXAMPLE of overriding at least one base class method
    def stats(self):
            print("Don't touch my stats!")
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
        # This is where I would add code to detect file type and call appropriate child class or other function
       
if __name__ == "__main__":
    # main()
    # ****TESTING CASES***
    # COMMENT OUT TO RUN MAIN Function/command line input; UNCOMMENT main() func above
   
    # Create instance of base class
    gen_file = File("./resources/txt/example.txt")
    # gen_file.open() #So in this case I didn't build my base to independently run
    gen_file.stats()
    # gen_file.read() #So in this case I didn't build my base to independently run

    # # Create an instance of the  derived class TextProcessor
    text_file = TextProcessor("./resources/tx/example.txt")
    text_file.open()  
    text_file.stats() #file size(bytes), ...
    text_file.read() #this will cause an error if you don't have a text file

    print('-' * 40)
    # Create an instance of the  derived class ImageProcessor
    image_file = ImageProcessor("./resources/img/bmp/sunset.bmp", "Im_a_txt_file.txt (cough cough)")
    image_file.open()  
    image_file.stats() #file size(bytes), ...
    image_file.read()



