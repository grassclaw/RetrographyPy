

# variety of types to binary  
import sys


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

           if (len(sys.argv)) > 2:
               message = sys.argv[2]
               messageLen = len(message)
               messageToHide = bytearray(int.to_bytes(messageLen, 4, "big", signed=False))
               messageToHide.extend(map(ord, message))

               currentByte = pixelOffset
               myFile.seek(currentByte)
               for byteVal in messageToHide:
                   bitPos = 7
                   for bit in range(7):
                       # next bit of the message
                       currentBit = (byteVal >> bitPos) & 0x01

                       # clear the lsb
                       colorVal = image[currentByte] & 0xFE
                       # set the bit
                       colorVal = colorVal | currentBit
                       # save the new value
                       image[currentByte] = colorVal

                       bitPos -= 1
                       currentByte += 1

               # write the data to an output file
               with open('output.bmp', 'wb') as out:
                    out.write(image)

           print(myFile.read(1).hex())  

       else:
           print("File is not a BMP file.")
