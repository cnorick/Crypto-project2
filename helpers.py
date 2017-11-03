from Crypto.Util import number
from random import getrandbits
from fractions import gcd

'''
Object to hold keys. To use with enc/dec, only one of e and d may be specified.
'''
class Key (object):
    def __init__(self, numBits, N, e=None, d=None):
        if type(numBits) is not int:
            raise TypeError('numBits must be of type int. got type {}'.format(type(numBits)))
        if numBits <= 0:
            raise ValueError('numBits must be positive. got value {}'.format(numBits))
        if type(N) is not int:
            raise TypeError('N must be of type int. got type {}'.format(type(N)))

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
Only one of key.e and key.d may be specified.
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
        raise TypeError('n must be of type int. Got value {}'.format(type(n)))
    if n < 0:
        raise ValueError('n must be positive. Got value {}'.format(n))

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
Returns the multiplicative inverse of a mod N.
'''
def modInverse(a, N):
    g, x, y = egcd(a, N)
    if g != 1:
        raise Exception('No modular inverse')
    return x%N
