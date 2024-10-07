

# variety of types to binary  
import datetime
import random
import sys

def randomBit():
    #return a 0 or a 1 
    byteVal = random.randbytes(1)[0]
    bitVal = byteVal & 0x01
    return bitVal
    

# basic validation, make sure there is an argument    
if (len(sys.argv)) > 1:
    # open the input file
    with open(sys.argv[1], "rb") as myFile:
       
       # read the whole image for now
       image = bytearray(myFile.read())

       # read the 16 byte header
       rawBmpHeader = image[0:16]

       #dump the header
       print("BMP Header: " + rawBmpHeader.hex())

       # verify the Magic Number
       if (rawBmpHeader[0] == ord('B') and rawBmpHeader[1] == ord('M')):
           print("BM marker found!")

           # get the file size.  It's stored bytes 2-5, little endian 
           fileSize = (rawBmpHeader[5] << 24) + \
                      (rawBmpHeader[4] << 16) + \
                      (rawBmpHeader[3] << 8) + \
                      (rawBmpHeader[2])
           
           # get the offset of pixel data, bytes 10-13
           pixelOffset = (rawBmpHeader[13] << 24) + \
                         (rawBmpHeader[12] << 16) + \
                         (rawBmpHeader[11] << 8) + \
                         (rawBmpHeader[10])
           
           print("Image Size: " + str(fileSize))
           print("Pixel Offset: " + str(hex(pixelOffset)))

           # jump to the width and height 
           myFile.read(2)

           rawValue = image[18:21] 
           imageWidth = int.from_bytes(bytes(rawValue), "little")
           print("Image Width: " + str(imageWidth))

           rawValue = image[22:25]
           imageHeight = int.from_bytes(bytes(rawValue), "little", signed=True)
           print("Image Height: " + str(imageHeight))

           # seed the rng with current time
           random.seed(datetime.datetime.now().timestamp())

           currentByte = pixelOffset
           lastByte = pixelOffset + ((imageWidth * abs(imageHeight)) * 3)
           myFile.seek(currentByte)
           while (currentByte < lastByte): 
               #  Get a random bit
               randomLsb = randomBit()

               # save the new value
               currentValue = image[currentByte]

               # reset the lsb
               currentValue = currentValue & 0xFE

               # set LSB according to the random number 
               newValue = currentValue | randomLsb

               # set the new value
               image[currentByte] = newValue

               currentByte += 1

           # write the data to an output file
           with open(sys.argv[2], 'wb') as out:
                out.write(image)
                               
       else:
           print("File is not a BMP file.")
else:
    print("Usage: <input file> <outputfile>")
