import sys
from random import getrandbits
from Crypto.Util import number

'''
'''
class Key (object):
    def __init__(self, numBits, N, e=None, d=None):
        self.numBits = numBits
        self.N = N
        self.e = e
        self.d = d

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
    numMessageBits = key.numBits - numRandBits - 2
    r = getRandom(numRandBits)

    # Concat the randomness and the message.
    return (r << numMessageBits) | m

'''
Removes the randomness added to m by addRandom().
'''
def removeRandom(m, key):
    if type(key) is not Key:
        raise TypeError('key must be of type Key')
    if type(m) is not int:
        raise TypeError('m must be of type int')

    numRandBits = key.numBits // 2
    numMessageBits = key.numBits - numRandBits - 2

    # Remove the randomness from the message.
    return ((2 ** numMessageBits) - 1) & m

'''
Performs modular exponentiation.
Calculates [m^(key.ed) mod key.N].
'''
def modExp(m, key):
    if type(key) is not Key:
        raise TypeError('key must be of type Key')
    if type(m) is not int:
        raise TypeError('m must be of type int')
    ed = key.e if key.e != None else key.d
    return pow(m, ed, key.N)

'''
Returns a random n-bit prime number.
'''
def getPrime(n):
    if type(n) is not int:
        raise TypeError('n must be of type int')

    return number(n)

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

'''
decrypts <c> with private key <key>.
'''
def dec(c, key):
    if type(key) is not Key:
        raise TypeError('key must be of type Key')
    if type(c) is not int:
        raise TypeError('m must be of type int')

    mhat = modExp(c, key)

    return removeRandom(mhat, key)

'''
Creates a valid Key object.
'''
def keygen(n):
    return


def test():
    N = 3233
    numBits = 12
    for message in range(2**(numBits - numBits//2 - 2)):
        privKey = Key(12, N, e=413)
        pubKey = Key(12, N, d=17)
        e = enc(message, pubKey)
        d = dec(e, privKey)
        if d != message:
            print('d: {d}, message: {message}'.format(d=d, message=message))
            raise Exception("IT'S BROKEN")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("usage: python rsa-enc.py <e|d> <keyFile> <inputFile> <outputFile>")
        sys.exit()

    (mode, keyFileName, inputFileName, outputFileName) = sys.argv[1:5]

    with open(keyFileName, 'r') as keyFile:
        (numBits, N, ed) = [int(line) for line in keyFile.readlines()]

    with open(inputFileName, 'r') as inputFile:
        message = int(inputFile.read())

    if mode == 'e':
        output = enc(message, Key(numBits, N, e=ed))
    elif mode == 'd':
        output = dec(message, Key(numBits, N, d=ed))
    else:
        raise ValueError("mode must be e (encrypt) or d (decrypt)")
    
    with open(outputFileName, 'w') as outputFile:
        outputFile.write(str(output))
