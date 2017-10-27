import sys
from random import getrandbits

'''
ed is either e or d depending on whether or not the key is a public or private key.
'''
class Key (object):
    def __init__(self, numBits, N, ed):
        self.numBits = numBits
        self.N = N
        self.ed = ed

'''
Returns random int with r bits.
'''
def getRandom(r):
    return getrandbits(r)

'''
Adds randomness to the m and returns r||m of total bit length key.numBits.
Randomness is half of the total length.
'''
def addRandom(m, key):
    numRandBits = key.numBits // 2
    numMessageBits = key.numBits - numRandBits
    r = getRandom(numRandBits)

    # Concat the randomness and the message.
    return (r << numMessageBits) | m

'''
encrypts <m> with public key <key> in ZN*
'''
def enc(m, key):
    if type(key) is not Key:
        raise TypeError('key must be of type Key')
    
    mhat = addRandom(m, key)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("usage: python rsa-enc.py <keyFile> <inputFile> <outputFile>")
        sys.exit()

    (keyFileName, inputFileName, outputFileName) = sys.argv[1:4]

    with open(keyFileName, 'r') as keyFile:
        (numBits, N, e) = [int(line) for line in keyFile.readlines()]

    with open(inputFileName, 'r') as inputFile:
        message = int(inputFile.read())

    enc(message, Key(numBits, N, e))
    
    # with open(outputFileName, 'w') as outputFile:
    #     outputFile.write()
