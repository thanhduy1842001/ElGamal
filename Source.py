import numpy as np
import random
die = random.SystemRandom()
bits = 128

def single_test(n, a):
    exp = n - 1
    while not exp & 1:
        exp >>= 1
        
    if pow(a, exp, mod=n) == 1:
        return True
        
    while exp < n - 1:
        if pow(a, exp, mod=n) == n - 1:
            return True
            
        exp <<= 1
        
    return False
    
def millerRabin(n,k=40):
    for i in range(k):
        a = die.randrange(2, n - 1)
        if not single_test(n, a):
            return False
            
    return True

def genPrime():
    while True:
        a = (die.randrange(1 << bits - 1, 1 << bits) << 1) + 1
        if millerRabin(a):
            return a

def Bezout(a,b):
    m = a; xm = 1; ym = 0
    n = b; xn = 0; yn = 1
    while n!=0:
        q = m // n
        r = m % n
        xr = xm - q*xn
        yr = ym - q*yn
        m,xm,ym = n,xn,yn
        n,xn,yn = r,xr,yr
    if xm<0: xm += b
    return xm

def genKey():
    p = genPrime()
    g = np.random.randint(bits)
    privateKey = np.random.randint(bits)
    h = pow(g,privateKey,mod=p)
    publicKey = (g,p,h)
    return publicKey,privateKey

def encrypt(m,publicKey):
    y = np.random.randint(bits)
    (g,p,h) = publicKey
    c1 = pow(g,y,mod=p)
    c2 = (m * h**y) % p
    return (c1,c2)

def decrypt(c,publicKey,privateKey):
    (g,p,h) = publicKey
    (c1,c2) = c
    c1 = pow(c1,privateKey,mod=p)
    m = c2*Bezout(c1,p) % p
    return m

# test
# print("Input m: ",end="")
# m = int(input())

# publicKey, privateKey = genKey()
# print(f'publicKey = {publicKey}')
# print(f'privateKey = {privateKey}')

# c = encrypt(m,publicKey)
# print(f'c = {c}')

# m = decrypt(c,publicKey,privateKey)
# print(f'm = {m}')

# print("Press enter to exit...")
# i = input()