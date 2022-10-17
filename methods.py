import random
import numpy as np
import bitarray

RED_CHANNEL = 0
GREEN_CHANNEL = 1
BLUE_CHANNEL = 2
END_SYMBOL = '\0'
END_SYMBOL_BITS = bitarray.bitarray()
END_SYMBOL_BITS.frombytes((END_SYMBOL).encode('utf-8'))
END_SYMBOL_BITS_LENGTH = len(END_SYMBOL_BITS)


def getBrightness(pixel):
    return 0.2989 * pixel[RED_CHANNEL] + 0.5862 *  pixel[GREEN_CHANNEL] + 0.11448 * pixel[BLUE_CHANNEL]

def encrypt(image, key, countRepeat, brightness, information):
    output = image.copy()
    random.seed(key)
    height, width, channels = image.shape
    bitsInformation = bitarray.bitarray()
    bitsInformation.frombytes((information + END_SYMBOL).encode('utf-8'))
    for bitInformation in bitsInformation:
        for repeatIndex in range(countRepeat):
            i = int(random.random() * height) # i = random.randint(0, width - 1)
            j = int(random.random() * width) # j = random.randint(0, height - 1)
            pixel = image[i,j]
            lambdaxy = getBrightness(pixel)

            Bxy_new = pixel[BLUE_CHANNEL] + (2 * bitInformation - 1) * brightness * lambdaxy
            if Bxy_new < 0:
                Bxy_new = 0
            elif Bxy_new > 255:
                Bxy_new = 255
            output[i, j, BLUE_CHANNEL] = Bxy_new
    return output


def decrypt(image, key, countRepeat, brightness, blockSize):
    random.seed(key)
    height, width, channels = image.shape
    bits = ''

    def calculateAverageBlueChannel(targetHeightIndex, targetWidthIndex):
        BxyAll = 0
        count = 0
        for widthIndex in range(targetWidthIndex - blockSize, targetWidthIndex + blockSize):
            if widthIndex < 0 or widthIndex >= width:
                continue
            BxyAll += image[targetHeightIndex, widthIndex, BLUE_CHANNEL]
            count += 1

        for heightIndex in range(targetHeightIndex - blockSize, targetHeightIndex + blockSize):
            if heightIndex < 0 or heightIndex >= height:
                continue
            BxyAll += image[heightIndex, targetWidthIndex, BLUE_CHANNEL]
            count += 1
        return (BxyAll - 2 * image[targetHeightIndex, targetWidthIndex, BLUE_CHANNEL]) / (count - 2)

    count = 0
    while not checkItIsEnd(bits) and count < 2**15:
        q = 0
        for repeatIndex in range(countRepeat):
            i = int(random.random() * height) # i = random.randint(0, width - 1)
            j = int(random.random() * width) # j = random.randint(0, height - 1)
            q += image[i, j, BLUE_CHANNEL] - calculateAverageBlueChannel(i, j)

        if q > 0:
            bits += '1'
        else:
            bits += '0'

        count += 1
    try:
        return bitarray.bitarray(bits).tobytes().decode('utf-8')
    except UnicodeDecodeError:
        return bits


def checkItIsEnd(bits):
    length = len(bits)
    if length % 8 != 0 or length < END_SYMBOL_BITS_LENGTH:
        return False
    return  bitarray.bitarray(bits[-END_SYMBOL_BITS_LENGTH:]) == END_SYMBOL_BITS
