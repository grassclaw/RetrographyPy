
import os
import png, array
import sys
from os import system, name 
from collections import OrderedDict
from time import sleep, time

''' 3rd Party Library '''
from PIL import Image

# Create Random Seed based on current time
import random

#
# furtive - attempting to avoid notice or attention, 
#           typically because of guilt or a belief that 
#           discovery would lead to trouble; secretive
class furtivePy:
    width = 0
    height = 0
    imageType = "unknown"

    def __init__(self, startRow = 0, startCol = 0) -> None:
        self.width  = 0
        self.height = 0
        self.Pix    = None
        self.imageType = None
        self.startRow = startRow
        self.startCol = startCol
        
        self.usedPixelList = []

    def open(srcMedia, startRow = 0, startCol = 0):
        if (srcMedia.lower().endswith(".bmp")):
            return furtivePyBmp(srcMedia, startRow, startCol)
        elif (srcMedia.lower().endswith(".png")):
            return furtivePyPng(srcMedia, startRow, startCol)
        else:
            raise Exception("Incompatible image format.")

    def GetPixel(self, col, row):
        pass

    def UpdatePixel(self, r, g, b, col, row):
        pass

    def ExtractAlteredPixels(self, baseImageFile):
        
        self.recoveredMessage = []
        
        baseImage = furtivePy.open(baseImageFile)
        
        for row in range(0, self.height):
            for col in range(0, self.width):

                basePix = baseImage.GetPixel(col, row)
                covertPix = self.GetPixel(col, row)

                if basePix != covertPix:                    
                    redPix = covertPix[0]
                    grnPix = covertPix[1]
                    bluPix = covertPix[2]       
                    
                    redLSB = redPix & 0b00000001
                    grnLSB = grnPix & 0b00000001
                    bluLSB = bluPix & 0b00000001
                    
                    codeIndex = redLSB*4 + grnLSB*2 + bluLSB*1
                    
                    self.recoveredMessage.append(codeBook[codeIndex])

    def PrintResults(self):
        print("\n=============== Recovered Messages =================\n")
        indentLevel = 1
        for eachCodebookEntry in self.recoveredMessage:
            print(" "*(indentLevel*2), "Step:", indentLevel, "->", eachCodebookEntry[2:])
            indentLevel+=1
            
    def AlterPixelLinear(self, lsbs):
        # find a pixel that does not match the LSB r, g, b values provided 
        for row in range(self.startRow, self.height):
            for col in range(self.startCol, self.width):
                if (self.ProcessPixel(col, row, lsbs) == True):
                    return

    def ProcessPixel(self, col, row, lsbs):
        r = lsbs[0]
        g = lsbs[1]
        b = lsbs[2]

        pixel = self.GetPixel(col, row)

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
            self.UpdatePixel(redPix, grnPix, bluPix, col, row)

            self.usedPixelList.append([col, row, ])
            
            self.startRow = row + 1
            # advance the starting row for the next search
            
            return True
        return False
    
    def Save(self, fileName):  
        pass      
    def hide(self):
        print(self.imageType)
        pass

    def reveal():
        pass

class furtivePyBmp(furtivePy):
    def __init__(self, srcImage, startRow=0, startCol=0):
        super().__init__(startRow, startCol)
        self.img    = Image.open(srcImage)
        self.width  = self.img.width
        self.height = self.img.height
        self.Pix    = self.img.load()
        self.imageType = "bmp"

    def GetPixel(self, col, row):
        return self.Pix[col, row]  # Pixel Values Original
    def UpdatePixel(self, r, g, b, col, row):
        pixelValue = (r, g, b)
        self.Pix[col, row, ] = pixelValue
        return
    def Save(self, fileName):        
        # Save this as a new image
        try:
            self.img.save(fileName)
            return True
        except Exception as err:
            print("Error Saving Image: "+str(err))
            return False

class furtivePyPng(furtivePy):
    def __init__(self, srcImage, startRow=0, startCol=0):
        super().__init__(startRow, startCol)
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

    def GetPixel(self, col, row):
        pixelPosition = row + col * self.width
        pixel = self.Pix[pixelPosition * self.bytesPerPixel : (pixelPosition + 1) * self.bytesPerPixel]
        return pixel
    
    def UpdatePixel(self, r, g, b, col, row):
        pixelPosition = row + col * self.width
        altPixel = (r, g, b, 0) if self.metadata['alpha'] else (r, g, b)
        self.Pix[pixelPosition * self.bytesPerPixel : 
                 (pixelPosition + 1) * self.bytesPerPixel] = array.array('B', altPixel)
        return

    def Save(self, fileName):        
        # Save this as a new image
        try:
            outputImage = open(fileName, 'wb')

            # remove the physical entry in metadata
            del self.metadata['physical']
            writer = png.Writer(self.width, self.height, **self.metadata)

            writer.write_array(outputImage, self.Pix)
            return True
        except Exception as err:
            print("Error Saving Image: "+str(err))
            return False

furtivePy.open = staticmethod(furtivePy.open)
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
    covertObj = furtivePy.open(carrierFile)
    
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

                # test the recovery
                covertObj.ExtractAlteredPixels(carrierFile)
                covertObj.PrintResults()
                break
            
        elif selection == 99:
            sys.exit("\n\nOperation Aborted by User")      
        
        else:
            if rnd == 'L':
                covertObj.AlterPixelLinear(LSB_LIST[selection])   
            else:
                covertObj.AlterPixelRandom(LSB_LIST[selection])  
                
            msgList.append(codeBook[selection])
 

