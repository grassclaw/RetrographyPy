'''
WK-10 
Extraction of Covert Messages
Professor Hosmer
November 2020
'''

import png, array
import sys
import os
from collections import OrderedDict


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

codeBook[0] = '0-Dead Drop @'
codeBook[1] = '1-Corner of Lexington Ave and E 48th Street'
codeBook[2] = '2-Corner of Madison Ave and E 34th Street'
codeBook[3] = '3-Drop Package in Potted Plant outside Wells Fargo'
codeBook[4] = '4-Drop Package in Gold Gargage Can'
codeBook[5] = '5-12 PM Sharp'
codeBook[6] = '6-7 AM Sharp'
codeBook[7] = '7-Abort if you see a Red Rose'

def clear():
    for i in range(0, 2):
        print()            

class EXTRACT_CONTENT:
    ''' COVERT Image Creation Class '''
    def __init__(self, baseImage, covertImage):
        
        try:
            if (baseImage.lower().endswith(".bmp")):
                self.baseImg   = Image.open(baseImage)
                self.covertImg = Image.open(covertImage)
                self.height    = self.baseImg.height
                self.width     = self.baseImg.width
                self.basePIX   = self.baseImg.load()
                self.covertPIX = self.covertImg.load()
                self.imageType = "bmp"


            elif (baseImage.lower().endswith(".png")):
                # obtain a reader that reads a test file
                imageReader = png.Reader(filename=baseImage)

                # read all of the data in, see docs for read flat
                w, h, pixels, metadata = imageReader.read_flat()
                self.width  = w
                self.height = h
                self.basePix    = pixels
                self.bytesPerPixel = 4 if metadata['alpha'] else 3
                self.metadata = metadata
                self.imageType = "png"

                # open the covert file
                imageReader = png.Reader(filename=covertImage)
                # read all of the data in, see docs for read flat
                w, h, pixels, metadata = imageReader.read_flat()
                self.covertPIX = pixels
            else:
                raise Exception("Incompatible image format.")
            
        except Exception as err:
            sys.exit(str(err))
        
        self.usedPixelList = []
        
    def ExtractAlteredPixels(self):
        
        self.recoveredMessage = []
        
        for row in range(0, self.height):
            for col in range(0, self.width):
                pixelPosition = row + col * self.width

                if self.imageType == "bmp":
                    basePix   = self.basePIX[col, row]
                    covertPix = self.covertPIX[col, row]
                else:
                    basePix = self.basePix[pixelPosition * self.bytesPerPixel : (pixelPosition + 1) * self.bytesPerPixel]
                    covertPix = self.covertPIX[pixelPosition * self.bytesPerPixel : (pixelPosition + 1) * self.bytesPerPixel]
                
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

                     
if __name__ == '__main__':
    
    # Create PixelSearch Object
    print("\nExtracting Covert Message Ver .50\n")
    
    carrierFile = input("\nSelect Carrier File: ")
    covertFile = input("\nSelect Covert File: ")
    
    if not os.path.isfile(covertFile):
        sys.exit("\nInvalid Covert File\n")
        
    covertObj = EXTRACT_CONTENT(carrierFile, covertFile)
    covertObj.ExtractAlteredPixels()
    covertObj.recoveredMessage.sort()
    covertObj.PrintResults()

        
    
