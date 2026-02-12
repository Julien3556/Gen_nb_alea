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
    Convertit un nombre entier en sa représentation binaire sous forme de chaîne.
    
    Args:
        n (int): Nombre entier à convertir
    
    Returns:
        str: Représentation binaire du nombre sous forme de chaîne
    """
    return bin(n)[2:]

def shift_right(n, bits):
    """
    Décale un nombre vers la droite d'un nombre spécifié de bits.
    
    Args:
        n (int): Nombre à décaler
        bits (int): Nombre de bits pour le décalage
    
    Returns:
        int: Résultat du décalage vers la droite
    """
    return n >> bits

def shift_left(n, bits):
    """
    Décale un nombre vers la gauche d'un nombre spécifié de bits.
    
    Args:
        n (int): Nombre à décaler
        bits (int): Nombre de bits pour le décalage
    
    Returns:
        int: Résultat du décalage vers la gauche
    """
    return n << bits

def A(x):
    """
    Applique la transformation A du Mersenne Twister selon la parité de x.
    
    Si x est pair, retourne le décalage vers la droite. 
    Si x est impair, applique également un XOR avec la constante 0x9908B0DF (a).
    
    Args:
        x (int): Entier 32-bits à transformer
    
    Returns:
        int: Résultat de la transformation A(x)
    """
    if x % 2 == 0:
        return shift_right(x, 1) ^ 0x00000000 # Xor avec 0
    else:
        return shift_right(x, 1) ^ 0x9908B0DF # Xor avec a = 2567483615

def initialization(seed):
    """
    Initialise le vecteur d'état X du Mersenne Twister à partir d'une graine.
    
    Crée un tableau de 624 nombres 32-bits.
    
    Args:
        seed (int): Graine pour l'initialisation
    
    Returns:
        list: Liste de 624 entiers 32-bits constituant l'état initial
    """
    X = []
    X.append(seed)
    for i in range(1, n):
        temp = (1812433253 * (X[i-1] ^ shift_right(X[i-1], 30)) + i) & 0xFFFFFFFF
        X.append(temp)
    return X

def recurrence(X):
    """
    Applique l'opération de récurrence du Mersenne Twister.
    
    Args:
        X (list): État courant du Mersenne Twister (liste de 624 entiers)
    
    Returns:
        list: État mis à jour après application de la récurrence
    """
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
    """
    Applique l'étape de tempering du Mersenne Twister pour améliorer la distribution.
    
    Effectue une série de décalages et d'opérations XOR avec des constantes
    pour améliorer les propriétés statistiques du nombre généré.
    
    Args:
        y (int): Entier 32-bits à transformer
    
    Returns:
        int: Nombre transformé après tempering
    """
    # Opération de tempering
    y = y ^ (shift_right(y, u))
    y = y ^ ((shift_left(y, s)) & b)
    y = y ^ ((shift_left(y, t)) & c)
    y = y ^ (shift_right(y, l))

    return y

def mersenne_twister_test(seed, nb):
    """
    Génère des nombres aléatoires avec le Mersenne Twister à partir d'une graine.
    
    Args:
        seed (int): Graine pour initialiser le générateur
        nb (int): Nombre de valeurs aléatoires à générer
    
    Returns:
        list: Liste de nb nombres aléatoires 32-bits
    """
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
    """
    Génère des nombres aléatoires avec le Mersenne Twister en ignorant les premiers éléments.
    
    Génère nieme + nb nombres aléatoires et retourne seulement les nb derniers.
    Cela permet de simuler l'avancement interne du générateur avant de retourner les nombres.
    
    Args:
        seed (int): Graine pour initialiser le générateur
        nb (int): Nombre de valeurs aléatoires à retourner
        nieme (int): Nombre de valeurs à ignorer avant de retourner (par défaut, une valeur aléatoire)
    
    Returns:
        list: Liste de nb nombres aléatoires 32-bits après avoir ignoré nieme valeurs
    """
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

