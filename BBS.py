"""
Blum-Blum-Shub (BBS)
Utilise Mersenne Twister pour générer les nombres premiers et la graine
"""

from Mersenne_Twister import mersenne_twister


def est_premier(nombre):
    """Vérifie si un nombre est premier en testant tous les diviseurs de 2 à sqrt(nombre) c'est long mais sûr"""
    if nombre < 2:
        return False
    if nombre == 2:
        return True
    if nombre % 2 == 0:
        return False
    
    diviseur = 3
    while diviseur * diviseur <= nombre:
        if nombre % diviseur == 0:
            return False
        diviseur += 2
    return True


def generer_premier_blum(nb_bits, seed):
    """
    Génère un nombre premier p tel que p ≡ 3 (mod 4)
    On utilise Mersenne Twister pour générer des candidats
    """
    nombres_mt = mersenne_twister(seed, 500)
    
    for i in range(len(nombres_mt) - 2):
        # On combine 2 nombres de mersenne_twister pour avoir assez de bits
        
        candidat = (nombres_mt[i] << 32) | nombres_mt[i + 1]
        candidat = candidat % (2 ** nb_bits)
        
        # On force le bit de poids fort à 1 pour garantir la taille
        # Et on modifie les 2 derniers bits pour avoir ≡ 3 (mod 4)
        # car 3 en binaire = 11, donc on force les 2 derniers bits à 11
        candidat |= (1 << (nb_bits - 1))
        candidat = (candidat & ~0b11) | 0b11
        
        if est_premier(candidat):
            return candidat
    
    return None


def pgcd(a, b):
    """Calcule le PGCD de a et b avec l'algorithme d'Euclide"""
    while b:
        a, b = b, a % b
    return a


def bbs(nb_bits, seed, nombre_bit_alea):
    """
    Génère les paramètres pour BBS et retourne des nombres aléatoires
    """
    print("Génération de p et q...")
    
    # On génère deux nombres premiers de Blum différents
    p = generer_premier_blum(nb_bits, seed)
    q = generer_premier_blum(nb_bits, seed + 100)
    
    # On s'assure que p et q sont différents
    while p == q:
        q = generer_premier_blum(nb_bits, seed + 200)
    n = p * q
    
    # On génère x0 qui doit être coprime avec n
    nombres_mt = mersenne_twister(seed, 10)
    for val in nombres_mt:
        graine_x0 = 2 + (val % (n - 3))
        if pgcd(graine_x0, n) == 1:
            break
    
    # Premier état : x1 = x0**2 mod n
    etat_x = pow(graine_x0, 2, n)
    
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"n = {n}")
    print(f"x0 = {etat_x}")
    
    # Afin de tester on génère 10 nombres de la valeur de nombre_bit_alea
    print(f"\n 10 nombres aléatoires de {nombre_bit_alea} bits :")
    for i in range(10):
        j = 0
        for _ in range(nombre_bit_alea):
            bit = etat_x & 1
            etat_x = pow(etat_x, 2, n)  # x = x**2 mod n
            j = (j << 1) | bit
        print(j)
        


if __name__ == "__main__":
    print("=== Blum-Blum-Shub ===\n")
    
    seed = 123 # A modifier a chaque éxécution si on veut p,q différents
    bits = 32
    nombre_bit_alea = 16 # Permet de modifier la taille des nombres aléatoire qu'on génére
    bbs(bits, seed,nombre_bit_alea)