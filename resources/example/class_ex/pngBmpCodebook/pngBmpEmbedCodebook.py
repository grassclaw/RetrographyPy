
'''
WK-10 
Insertion of Covert Messages
Professor Hosmer
November 2020

Added PNG support with PyPng 
Professor Duren
September 2023
'''
import os
import png, array
import sys
from os import system, name 
from collections import OrderedDict
from time import sleep, time

# Create Random Seed based on current time
import random
random.seed(time())


''' 3rd Party Library '''
from PIL import Image

'''
Image Orientation

         |
         |
y (rows) |
         |
         |     
         -----------------------------
                     x (columns)
'''
# Pixel tuple index
RED   = 0
GREEN = 1
BLUE  = 2

codeBook = OrderedDict()

codeBook[0] = 'Dead Drop @'
codeBook[1] = 'Corner of Lexington Ave and E 48th Street'
codeBook[2] = 'Corner of Madison Ave and E 34th Street'
codeBook[3] = 'Drop Package in Potted Plant outside Wells Fargo'
codeBook[4] = 'Drop Package in Gold Gargage Can'
codeBook[5] = '12 PM Sharp'
codeBook[6] = '7 AM Sharp'
codeBook[7] = 'Abort if you see a Red Rose'

def clear():
    for i in range(0, 2):
        print()

        
def DisplayMenu(msgSoFar):
    clear()
    validChoices = [0,1,2,3,4,5,6,7,55,99]
    
    while True:
        if msgSoFar:
            print("\nCovert Message Contents So Far")
            for eachEntry in msgSoFar:
                print("\t"+eachEntry)
            print()
    
        for key, value in codeBook.items():
            print('['+str(key)+']  ', value)
        print()
        print('[55]  ', 'Create New Image')
        print('[99]  ', 'Quit Do Not Save')
        
        try:
            sel = int(input("\nSelect Message 0-7 to Hide (or 55 When ready to finalize) "))
            if sel in validChoices:
                return sel
            else:
                print("Invalid Selection ...\n")
        except:
            print("Invalid Selection ...\n")
            

class COVERT_IMG:
    ''' COVERT Image Creation Class '''
    def __init__(self, srcImage, startRow=0, startCol=0):
        
        try:
            if (srcImage.lower().endswith(".bmp")):
                self.img    = Image.open(srcImage)
                self.width  = self.img.width
                self.height = self.img.height
                self.Pix    = self.img.load()
                self.imageType = "bmp"
            elif (srcImage.lower().endswith(".png")):
                # obtain a reader that reads a test file
                imageReader = png.Reader(filename=srcImage)

                # read all of the data in, see docs for read flat
                w, h, pixels, metadata = imageReader.read_flat()
                self.width  = w
                self.height = h
                self.Pix    = pixels
                self.bytesPerPixel = 4 if metadata['alpha'] else 3
                self.metadata = metadata
                self.imageType = "png"
            else:
                raise Exception("Incompatible image format.")
            
        except Exception as err:
            sys.exit(str(err))
    
        self.startRow = startRow
        self.startCol = startCol
        
        self.usedPixelList = []
        
    def AlterPixelLinear(self, lsbs):
        
        
        # find a pixel that does not match the LSB r, g, b values provided 
        for row in range(self.startRow, self.height):
            for col in range(self.startCol, self.width):
                self.ProcessPixel(col, row, lsbs)
                return
                
    def ProcessPixel(self, col, row, lsbs):

        r = lsbs[0]
        g = lsbs[1]
        b = lsbs[2]

        if (self.imageType == "png"):
            pixelPosition = row + col * self.width
            pixel = self.Pix[pixelPosition * self.bytesPerPixel : (pixelPosition + 1) * self.bytesPerPixel]
        else:
            pixel = self.Pix[col, row]  # Pixel Values Original
        
        # extract the red, green and blue pixel values
        redPix = pixel[0]
        grnPix = pixel[1]
        bluPix = pixel[2]
        
        # Obtain the LSB of each
        
        redLSB = redPix & 0b00000001
        grnLSB = grnPix & 0b00000001
        bluLSB = bluPix & 0b00000001
        
        # we are looking for the first pixel that 
        # differs in either R, G, or B LSB
        
        if r != redLSB or g != grnLSB or b != bluLSB:
            # We got one
            redPix = pixel[0]
            grnPix = pixel[1]
            bluPix = pixel[2]
            
            # Alter the Pixel RGB
            if r == 0:
                redPix = redPix & 0b11111110
            else:
                redPix = redPix | r
            
            if g == 0:
                grnPix = grnPix & 0b11111110
            else:
                grnPix = grnPix | g
                
            if b == 0:
                bluPix = bluPix & 0b11111110
            else:
                bluPix = bluPix | b            
            
            # Update the pixel
            if (self.imageType == "png"):
                altPixel = (redPix, grnPix, bluPix, 0) if self.metadata['alpha'] else (redPix, grnPix, bluPix)
            else:
                altPixel = (redPix, grnPix, bluPix)
            
            # Save the changed Pixel in the pixel proper
            if (self.imageType == "png"):
                self.Pix[pixelPosition * self.bytesPerPixel : 
                         (pixelPosition + 1) * self.bytesPerPixel] = array.array('B', altPixel)
            else:
                self.Pix[col, row] = altPixel

            self.usedPixelList.append([col, row])
            
            self.startRow = row + 1
            # advance the starting row for the next search
            
            return

    def AlterPixelRandom(self, lsbs):
        
        r = lsbs[0]
        g = lsbs[1]
        b = lsbs[2]

        while True:
            row = random.randint(0, self.height-1)
            col = random.randint(0, self.width-1)
            
            if [col, row] in self.usedPixelList:
                # Don't re-use pixels
                continue
            
            self.ProcessPixel(col, row, lsbs)
            return
                
    def Save(self, fileName):        
        # Save this as a new image
        try:
            if (self.imageType == "png"):
                outputImage = open(fileName, 'wb')

                # remove the physical entry in metadata
                del self.metadata['physical']
                writer = png.Writer(self.width, self.height, **self.metadata)

                writer.write_array(outputImage, self.Pix)
            else:
                self.img.save(fileName)

            return True
        except Exception as err:
            print("Error Saving Image: "+str(err))
            return False
        
                    
if __name__ == '__main__':
    
    # Create a list of R,G,B values we need to hide
    LSB_LIST = [ [0,0,0], [0,0,1], [0,1,0], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1] ]
                 
    msgList = []
    locList = []
    
    print("\nCovert Message Creation for True Color RGB Images Ver .50\n")
    
    # Create PixelSearch Object
    carrierFile = input("\nSelect Carrier File: ")
    
    if not os.path.isfile(carrierFile):
        sys.exit("\nInvalid Carrier File\n")
        
    # Create PixelSearch Object
    covertObj = COVERT_IMG(carrierFile)
    

    while True:
        rnd = input("Select  R = Random Placement  L = linear Placement >> ")
        rnd = rnd.upper()
        if not rnd in ['R','L']:
            print("\nInvalid Selection ... Please Choose either R or L\n")
        else:
            break
    
    while True:

        selection = DisplayMenu(msgList)
        
        if selection == 55:
            fileName = input("\nSpecify Output Covert Filename i.e. Secret.PNG : ")
            result = covertObj.Save(fileName)
            if not result:
                print("Try Again\n")
                continue
            else:
                print("Covert Image Created \n")
                print("Altered Pixel List")
                for eachRC in covertObj.usedPixelList:
                    print(eachRC)
                print("\n\nScript Complete .. Bye\n")
                break
            
        elif selection == 99:
            sys.exit("\n\nOperation Aborted by User")      
        
        else:
            if rnd == 'L':
                covertObj.AlterPixelLinear(LSB_LIST[selection])   
            else:
                covertObj.AlterPixelRandom(LSB_LIST[selection])  
                
            msgList.append(codeBook[selection])
            

 