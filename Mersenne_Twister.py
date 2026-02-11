"""
Source : https://www.planchet.net/EXT/ISFA/fp-isfa.nsf/0/6CEB5B474CD3B563C125700C0040D8E3/$FILE/GT2008-01.pdf?OpenElement
"""
import Gen_systeme
# Paramètres MT19937
w = 32  # longueur en bits
n = 624  # ordre de récurrence
r = 31
m = 397
a = 2567483615  # 0x9908B0DF


def int_to_bin(n):
    """
    """
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

def initialization(seed):
    X = []
    X.append(seed)
    for i in range(1, n):
        temp = (1812433253 * (X[i-1] ^ shift_right(X[i-1], 30)) + i) & 0xFFFFFFFF
        X.append(temp)
    return X

def recurrence(X):
    M_r = 0x7FFFFFFF # où les r (31) premiers bits valent 1, les autres 0
    M_r_complement = 0x80000000 # où les r (31) derniers bits valent 1, les autres 0
    
    for k in range(n):
        x = (X[k] & M_r_complement) | (X[(k+1) % n] & M_r)
        xA = A(x)
        X[k] = X[(k + m) % n] ^ xA
    return X

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

def mersenne_twister_test(seed, nb):
    X = initialization(seed)
    numbers = []
    index = 0
    
    for i in range(nb):
        if index == 0:
            X = recurrence(X)
        
        y = tempering(X[index])
        numbers.append(y)
        
        index = (index + 1) % n
    return numbers

def mersenne_twister(seed, nb, nieme=Gen_systeme.return_small_number()):
    #print("nieme =", nieme)
    X = initialization(seed)
    numbers = []
    index = 0
    
    for i in range(nieme + nb):
        if index == 0:
            X = recurrence(X)
        
        y = tempering(X[index])
        numbers.append(y)
        
        index = (index + 1) % n
    return numbers[nieme:]

if __name__ == "__main__":
    marseenne_seed = 123  # Valeur de seed par défaut

    nb = 0  # Nombre de nombres aléatoires à générer"

    # Test de générations de nb nombres aléatoires
    numbers = mersenne_twister_test(marseenne_seed, 10)
    print("Nombres aléatoires générés par le Mersenne Twister :")
    for el in numbers:
        print(el)

        # Affichage en binaire
        print(int_to_bin(el))

    # Génération du nième nombre aléatoire
    numbers = mersenne_twister(marseenne_seed, 10)
    for el in numbers:
        print(el)

