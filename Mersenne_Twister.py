"""
Source : https://www.planchet.net/EXT/ISFA/fp-isfa.nsf/0/6CEB5B474CD3B563C125700C0040D8E3/$FILE/GT2008-01.pdf?OpenElement
"""
# Paramètres MT19937
w = 32  # longueur en bits
n = 624  # ordre de récurrence
r = 31
m = 397
a = 2567483615  # 0x9908B0DF

# Paramètres de tempering
u = 11
s = 7
t = 15
l = 18
b = 2636928640   # 0x9D2C5680
c = 4022730752   # 0xEFC60000

def int_to_bin(n):
    return bin(n)[2:]

def shift_right(n, bits):
    return n >> bits

def shift_left(n, bits):
    return n << bits

def A(x):
    if x % 2 == 0:
        return shift_right(x, 1) ^ 0x00000000 # Xor avec 0
    else:
        return shift_right(x, 1) ^ 0x9908B0DF # Xor avec a = 2567483615

def recurrence(n, seed):
    Mr = 11111111111111111111111111111110 # où les r (31) premiers bits valent 1, les autres 0
    nonMr = 01111111111111111111111111111111 # où les r (31) premiers bits valent 0, les autres 1


    X = []
    X_n = seed
    X.append(X_n)
    for i in range(n):
        X_n = A()

# Paramètres de tempering
u = 11
s = 7
t = 15
l = 18
b = 0x9D2C5680   # 2636928640
c = 0xEFC60000   # 4022730752
def tempering(y):
    # Opération de tempering
    y = y ^ (shift_right(y, u))
    y = y ^ ((shift_left(y, s)) & b)
    y = y ^ ((shift_left(y, t)) & c)
    y = y ^ (shift_right(y, l))

    return y

if __name__ == "__main__":
    n = 5
    binary = int_to_bin(n)
    print(f"Binaire de {n}: {binary}")

