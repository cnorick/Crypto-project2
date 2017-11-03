import sys
from random import getrandbits
from Crypto.Util import number
from fractions import gcd

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
    if key.e != None and key.d != None:
        raise ValueError('it is ambiguous whether key is private or public')

    ed = key.e if key.e != None else key.d
    return pow(m, ed, key.N)

'''
Returns a random n-bit prime number.
'''
def getPrime(n):
    if type(n) is not int:
        raise TypeError('n must be of type int')

    return number.getPrime(n)

'''
Extended Euclidean Algorithm
return (g, x, y) a*x + b*y = gcd(x, y)
'''
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a,a)
    return (g, x - (b//a) * y, y)

'''
x = mulinv(b) mod n, (x * b) % n == 1
'''
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x%m

'''
encrypts <m> with public key <key> to element in ZN*.
m must not exceed key.n / 2 - 2 bits.
'''
def enc(m, key):
    if type(key) is not Key:
        raise TypeError('key must be of type Key')
    if type(m) is not int:
        raise TypeError('m must be of type int')
    
    # mhat is an element in ZN*.
    # print(bin(m))
    mhat = addRandom(m, key)
    # print(bin(mhat))
    print('enc {}'.format(mhat))
    print('enc post exp {}'.format(modExp(mhat, key)))

    return modExp(mhat, key)

'''
decrypts <c> with private key <key>.
'''
def dec(c, key):
    if type(key) is not Key:
        raise TypeError('key must be of type Key')
    if type(c) is not int:
        raise TypeError('m must be of type int')

    print('dec pre exp {}'.format(c))
    mhat = modExp(c, key)
    print('dec {}'.format(mhat))

    return removeRandom(mhat, key)

'''
Creates a valid Key object.
'''
def keygen(n):
    for i in range(10):
        p = getPrime(n // 2)
        q = getPrime(n // 2)

        if p != q:
            break;
    else:
        raise Exception('could not produce 2 unique primes after 10 tries.')

    N = p * q
    order = (p - 1) * (q - 1)

    smallPrimes = [3, 5, 7, 11, 13]
    for e in smallPrimes:
        if gcd(e, order) == 1:
            break;
    else:
        raise Exception('could not a small number coprime to {}.'.format(order))

    d = modinv(e, order)
    
    return Key(n, N, e=e, d=d)

def test():
    N = 3233
    numBits = 12
    for message in range(2**(numBits - numBits // 2 - 2)):
        privKey = Key(numBits, N, e=413)
        pubKey = Key(numBits, N, d=17)
        e = enc(message, pubKey)
        d = dec(e, privKey)
        if d != message:
            print('d: {d}, message: {message}'.format(d=d, message=message))
            raise Exception("IT'S BROKEN")

def testKeyGen():
    for numBits in range(12, 30):
        for message in range(3, 2**(numBits - numBits // 2 - 2) - 1):
            for i in range(10):
                k = keygen(numBits)
                # print('numBits {}, message: {}, k.d: {}, k.e: {}, k.N: {}'.format(numBits, message, k.d, k.e, k.N))
                assert (message ** (k.e * k.d)) % k.N == message

                privKey = Key(k.numBits, k.N, d=k.d)
                pubKey = Key(k.numBits, k.N, e=k.e)

                e = enc(message, pubKey)
                d = dec(e, privKey)
                if d != message:
                    print('numBits {}, d: {}, message: {}, k.d: {}, k.e: {}, k.N: {}'.format(numBits, d, message, k.d, k.e, k.N))
                    raise Exception("IT'S BROKEN")

if __name__ == "__main__":
    # if len(sys.argv) != 5:
    #     print("usage: python rsa-enc.py <e|d> <keyFile> <inputFile> <outputFile>")
    #     sys.exit()

    # (mode, keyFileName, inputFileName, outputFileName) = sys.argv[1:5]

    # with open(keyFileName, 'r') as keyFile:
    #     (numBits, N, ed) = [int(line) for line in keyFile.readlines()]

    # with open(inputFileName, 'r') as inputFile:
    #     message = int(inputFile.read())

    # if mode == 'e':
    #     output = enc(message, Key(numBits, N, e=ed))
    # elif mode == 'd':
    #     output = dec(message, Key(numBits, N, d=ed))
    # else:
    #     raise ValueError("mode must be e (encrypt) or d (decrypt)")
    
    # with open(outputFileName, 'w') as outputFile:
    #     outputFile.write(str(output))
    # test()
    testKeyGen()

    # m = 1
    # k = keygen(11)
    # r = addRandom(m, k)
    # a = removeRandom(m, k)

    # print(bin(m))
    # print(bin(r))
    # print(bin(a))

    # me = modExp(m, Key(k.numBits, k.N, k.e))

    # print(bin(me))