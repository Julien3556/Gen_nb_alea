"""
Blum-Blum-Shub (BBS)
Utilise Mersenne Twister pour générer les nombres premiers et la graine
"""

from Mersenne_Twister import mersenne_twister


def est_premier(nombre):
    """
    Vérifie si un nombre est premier en testant tous les diviseurs.
    
    Args:
        nombre (int): Nombre entier à vérifier
    
    Returns:
        bool: True si le nombre est premier, False sinon
    """
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
    Génère un nombre premier p tel que p ≡ 3 (mod 4).

    On utilise Mersenne Twister pour générer des candidats.
    
    Args:
        nb_bits (int): Nombre de bits désirés pour le nombre premier
        seed (int): Graine pour le générateur Mersenne Twister
    
    Returns:
        int or None: Un nombre premier de Blum de nb_bits bits, ou None si non trouvé
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
    """
    Calcule le PGCD de a et b avec l'algorithme d'Euclide
    
    Args:
        a (int): Premier nombre
        b (int): Deuxième nombre
    
    Returns:
        int: Le PGCD de a et b
    """
    while b:
        a, b = b, a % b
    return a


def bbs(nb_bits, seed, nombre_bit_alea, nombre_de_valeur):
    """
    Génère les parametres pour BBS et retourne des nombres aleatoires

    Args:
        nb_bits (int): Nombre de bits pour les nombres premiers p et q
        seed (int): Graine pour initialiser le générateur Mersenne Twister
        nombre_bit_alea (int): Nombre de bits pour chaque nombre aléatoire généré
        nombre_de_valeur (int): Nombre de valeurs aléatoires à générer
    
    Returns:
        list: Liste de nombre_de_valeur nombres aléatoires de nombre_bit_alea bits chacun
    """
    # print("Generation de p et q...")
    
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
    
    """
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"n = {n}")
    print(f"x0 = {etat_x}")
    """
    
    # Afin de tester on génère 10 nombres de la valeur de nombre_bit_alea
    nb = nombre_de_valeur
    """
    print(f"\nnb nombres aleatoires de {nombre_bit_alea} bits :")
    """
    res = []
    for i in range(nb):
        j = 0
        for _ in range(nombre_bit_alea):
            bit = etat_x & 1
            etat_x = pow(etat_x, 2, n)  # x = x**2 mod n
            j = (j << 1) | bit
        res.append(j)

    return res


if __name__ == "__main__":
    print("=== Blum-Blum-Shub ===\n")
    
    seed = 123 # A modifier a chaque éxécution si on veut p,q différents
    bits = 32
    nombre_bit_alea = 16 # Permet de modifier la taille des nombres aléatoire qu'on génére
    nb = 10
    res = bbs(bits, seed,nombre_bit_alea, nb)
    print(res)