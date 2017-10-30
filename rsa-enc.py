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
    if type(key) is not Key:
        raise TypeError('key must be of type Key')
    if type(m) is not int:
        raise TypeError('m must be of type int')

    numRandBits = key.numBits // 2
    numMessageBits = key.numBits - numRandBits
    r = getRandom(numRandBits)

    # Concat the randomness and the message.
    return (r << numMessageBits) | m

'''
Performs modular exponentiation.
Calculates [m^(key.ed) mod key.N].
'''
def modExp(m, key):
    if type(key) is not Key:
        raise TypeError('key must be of type Key')
    if type(m) is not int:
        raise TypeError('m must be of type int')

    return (m ** key.ed) % key.N

'''
encrypts <m> with public key <key> to element in ZN*.
'''
def enc(m, key):
    if type(key) is not Key:
        raise TypeError('key must be of type Key')
    if type(m) is not int:
        raise TypeError('m must be of type int')
    
    # mhat is an element in ZN*.
    mhat = addRandom(m, key)

    return modExp(mhat, key)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("usage: python rsa-enc.py <keyFile> <inputFile> <outputFile>")
        sys.exit()

    (keyFileName, inputFileName, outputFileName) = sys.argv[1:4]

    with open(keyFileName, 'r') as keyFile:
        (numBits, N, e) = [int(line) for line in keyFile.readlines()]

    with open(inputFileName, 'r') as inputFile:
        message = int(inputFile.read())

    print(enc(message, Key(numBits, N, e)))
    
    # with open(outputFileName, 'w') as outputFile:
    #     outputFile.write()
